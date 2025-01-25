from os import path, remove

from flask import Response, flash, jsonify, render_template, request, url_for
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from app.extensions import db, profile_imgs
from app.forms import (DeletePostForm, EditPostForm, EditProfileForm,
                       FollowProfileForm, PostForm)
from app.models import Post, User
from app.utils import get_post, optimize_img, redirect_to_referrer, flash_form_errors

from . import api


@api.route('/post/fetch', methods=['POST'])
@login_required
def fetch_post() -> ResponseReturnValue:
    status, resp = get_post(request.json)
    if status != 200:
        return Response(
            response=jsonify(resp).get_data(
                as_text=True),
            status=status,
            mimetype='application/json'
        )

    return render_template('components/post.html', post=resp)


@api.route('/post/add_like', methods=['POST'])
@login_required
def like_post() -> Response:
    status, resp = get_post(request.json)
    if status != 200:
        return Response(
            response=jsonify(resp).get_data(
                as_text=True),
            status=status,
            mimetype='application/json'
        )

    current_user.add_like(resp)
    db.session.commit()

    return Response(
        response=jsonify(
            {'status': 'success', 'message': 'Like added successfully'}).get_data(as_text=True),
        status=200,
        mimetype='application/json'
    )


@api.route('/post/remove_like', methods=['POST'])
@login_required
def remove_post() -> Response:
    status, resp = get_post(request.json)
    if status != 200:
        return Response(
            response=jsonify(resp).get_data(
                as_text=True),
            status=status,
            mimetype='application/json'
        )

    current_user.remove_like(resp)
    db.session.commit()

    return Response(
        response=jsonify(
            {'status': 'success', 'message': 'Like removed successfully'}).get_data(as_text=True),
        status=200,
        mimetype='application/json'
    )


@api.route('/post/create/', methods=['POST'])
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

@api.route('/post/edit/', methods=['POST'])
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


@api.route('/post/delete/', methods=['POST'])
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


@api.route('/profile/edit/', methods=['POST'])
def edit_profile() -> ResponseReturnValue:
    form: EditProfileForm = EditProfileForm()
    if form.validate_on_submit():
        if form.bio.data != current_user.bio and form.bio.data:
            current_user.bio = form.bio.data
            db.session.add(current_user)
            db.session.commit()
            flash('Profile bio changed', category='success')

        if form.image.data:
            img = optimize_img(form.image.data, resize=True)
            name = secure_filename(f'{current_user.id}_pfp.webp')

            if path.exists(img_path := profile_imgs.path(name)):
                remove(img_path)

            profile_imgs.save(img, name=name)
            flash('Profile picture updated!', category='success')
    elif form.errors:
        flash_form_errors(form)

    return redirect_to_referrer()


@api.route('/profile/follow', methods=['POST'])
def follow_profile() -> ResponseReturnValue:
    form: FollowProfileForm = FollowProfileForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(id = form.profile_id.data).first_or_404()
        current_user.follow(user)
        db.session.commit()

    elif form.errors:
        flash_form_errors(form)

    return redirect_to_referrer(fallback=url_for('core.profile', username=current_user.username))


@api.route('/profile/unfollow', methods=['POST'])
def unfollow_profile() -> ResponseReturnValue:
    form: FollowProfileForm = FollowProfileForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(id = form.profile_id.data).first_or_404()
        current_user.unfollow(user)
        db.session.commit()

    elif form.errors:
        flash_form_errors(form)

    return redirect_to_referrer(fallback=url_for('core.profile', username=current_user.username))