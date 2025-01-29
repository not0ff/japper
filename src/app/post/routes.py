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
    status, resp = get_post(request.args.to_dict())
    if status != 200:
        return jsonify(resp), status

    return render_template('post/post.html', post=resp)


@post.route('/add_like', methods=['POST'])
@login_required
def like_post() -> ResponseReturnValue:
    status, resp = get_post(request.json)
    if status != 200 or not isinstance(resp, Post):
        return jsonify(resp), status

    current_user.add_like(resp)
    add_notification(user=resp.author, content=f'{current_user.username} gave you aura!')
    db.session.commit()

    return 'Like added successfully', 200


@post.route('/get_likes')
@login_required
def get_likes() -> ResponseReturnValue:
    status, resp = get_post(request.args.to_dict())
    if status != 200:
        return jsonify(resp), status
    likes_users = None
    if isinstance(resp, Post):
        likes_users = [User.query.get(like.user_id) for like in resp.likes]

    return render_template('components/user_list.html', users=likes_users)


@post.route('/remove_like', methods=['POST'])
@login_required
def remove_post() -> ResponseReturnValue:
    status, resp = get_post(request.json)
    if status != 200:
        return jsonify(resp), status

    current_user.remove_like(resp)
    db.session.commit()

    return 'Like removed successfully', 200


@post.route('/create', methods=['POST'])
@login_required
def create_post() -> ResponseReturnValue:
    form: PostForm = PostForm()
    if form.validate_on_submit():
        post: Post = Post(user_id=current_user.id,
                          content=form.content.data)
        db.session.add(post)
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
