from os import path, remove

from flask import (Response, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required
from is_safe_url import is_safe_url
from werkzeug.utils import secure_filename

from app import db
from app.extensions import db, profile_imgs
from app.forms import DeletePostForm, EditPostForm, EditProfileForm, PostForm
from app.models import Post
from app.utils import get_post, optimize_img

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


@api.route('/post/create', methods=['POST'])
@login_required
def create_post() -> ResponseReturnValue:
    post_form: PostForm = PostForm()
    if post_form.validate_on_submit():
        post: Post = Post(user_id=current_user.id,
                          content=post_form.content.data)
        db.session.add(post)
        db.session.commit()

    elif post_form.errors:
        for field, errors in post_form.errors.items():
            for error in errors:
                flash(f'{field.capitalize()}: {error}', category='danger')

    next_page = request.referrer
    if next_page is not None and is_safe_url(next_page, {request.host}):
        return redirect(next_page)
    return redirect(url_for('core.feed'))


@api.route('/post/edit/', methods=['POST'])
@login_required
def edit_post() -> ResponseReturnValue:
    edit_post_form: EditPostForm = EditPostForm()
    if edit_post_form.validate_on_submit():
        post: Post = Post.query.filter_by(
            id=edit_post_form.post_id.data, user_id=current_user.id)
        post.update({Post.content: edit_post_form.content.data})

        db.session.commit()

    elif edit_post_form.errors:
        for field, errors in edit_post_form.errors.items():
            for error in errors:
                flash(f'{field.capitalize()}: {error}', category='danger')

    next_page = request.referrer
    if next_page is not None and is_safe_url(next_page, {request.host}):
        return redirect(next_page)
    return redirect(url_for('core.feed'))


@api.route('/post/delete/', methods=['POST'])
@login_required
def delete_post() -> ResponseReturnValue:
    delete_post_form: DeletePostForm = DeletePostForm()
    if delete_post_form.validate_on_submit():
        post: Post = Post.query.filter_by(
            id=delete_post_form.post_id.data, user_id=current_user.id).delete()

        db.session.commit()
    elif delete_post_form.errors:
        for field, errors in delete_post_form.errors.items():
            for error in errors:
                flash(f'{field.capitalize()}: {error}', category='danger')

    next_page = request.referrer
    if next_page is not None and is_safe_url(next_page, {request.host}):
        return redirect(next_page)
    return redirect(url_for('core.feed'))


@api.route('/profile/edit/', methods=['POST'])
def edit_profile() -> ResponseReturnValue:
    profile_form: EditProfileForm = EditProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.bio.data != current_user.bio and profile_form.bio.data:
            current_user.bio = profile_form.bio.data
            db.session.add(current_user)
            db.session.commit()
            flash('Profile bio changed', category='success')

        if profile_form.image.data:
            img = optimize_img(profile_form.image.data, resize=True)
            name = secure_filename(f'{current_user.id}_pfp.webp')

            if path.exists(img_path := profile_imgs.path(name)):
                remove(img_path)

            profile_imgs.save(img, name=name)  # type: ignore
            flash('Profile picture updated!', category='success')
    elif profile_form.errors:
        for field, errors in profile_form.errors.items():
            for error in errors:
                flash(f'{field.capitalize()}: {error}', category='danger')

    return redirect(url_for('core.profile', username=current_user.username))
