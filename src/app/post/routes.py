from flask import jsonify, render_template, request
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import DeletePostForm, EditPostForm, PostForm
from app.models import Post, User
from app.utils import (add_notification, flash_form_errors, get_post,
                       redirect_to_referrer)

from . import post


@post.route('/fetch')
@login_required
def fetch_post() -> ResponseReturnValue:
    post, status = get_post(request.args.to_dict())
    if status != 200:
        return jsonify(post), status

    return jsonify({'status': 'ok', 'result': {'post': render_template('post/post.html', post=post)}}), 200


@post.route('/add_like', methods=['POST'])
@login_required
def like_post() -> ResponseReturnValue:
    post, status = get_post(request.json)
    if status != 200 or not isinstance(post, Post):
        return jsonify(post), status
    
    current_user.add_like(post)
    if current_user != post.author:
        add_notification(user=post.author, content=f'{current_user.username} gave you aura!')
    db.session.commit()

    return jsonify({'status': 'ok'}), 200


@post.route('/get_likes')
@login_required
def get_likes() -> ResponseReturnValue:
    post, status = get_post(request.args.to_dict())
    if status != 200:
        return jsonify(post), status
    likes_users = None
    if isinstance(post, Post):
        likes_users = [User.query.get(like.user_id) for like in post.likes]

    return jsonify({'status': 'ok', 'result': {'userList': render_template('components/user_list.html', users=likes_users)}}), 200


@post.route('/remove_like', methods=['POST'])
@login_required
def remove_post() -> ResponseReturnValue:
    post, status = get_post(request.json)
    if status != 200:
        return jsonify(post), status

    current_user.remove_like(post)
    db.session.commit()

    return jsonify({'status': 'ok'}), 200


@post.route('/create', methods=['POST'])
@login_required
def create_post() -> ResponseReturnValue:
    form: PostForm = PostForm()
    if form.validate_on_submit():
        post: Post = Post(user_id=current_user.id,
                          content=form.content.data)
        db.session.add(post)
        for follower in current_user.followers:
            add_notification(user=follower, content=f'{current_user.username} has made a new post!')
        
        db.session.commit()

    elif form.errors:
        flash_form_errors(form)

    return redirect_to_referrer()


@post.route('/edit', methods=['POST'])
@login_required
def edit_post() -> ResponseReturnValue:
    form: EditPostForm = EditPostForm()
    if form.validate_on_submit():
        post: Post = Post.query.filter_by(
            id=form.post_id.data, user_id=current_user.id)
        post.update({Post.content: form.content.data})

        db.session.commit()
    elif form.errors:
        flash_form_errors(form)

    return redirect_to_referrer()


@post.route('/delete', methods=['POST'])
@login_required
def delete_post() -> ResponseReturnValue:
    form: DeletePostForm = DeletePostForm()
    if form.validate_on_submit():
        post: Post = Post.query.filter_by(
            id=form.post_id.data, user_id=current_user.id).delete()

        db.session.commit()
    elif form.errors:
        flash_form_errors(form)

    return redirect_to_referrer()
