from os import path, remove

import sqlalchemy as sa
from flask import (Response, flash, jsonify, redirect, render_template,
                   request, send_file, send_from_directory, url_for)
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required
from is_safe_url import is_safe_url
from werkzeug.utils import secure_filename

from app.extensions import db, profile_imgs
from app.forms import EditProfileForm, PostForm
from app.models import Post, User
from app.utils import optimize_img

from . import core


@core.route('/')
def index() -> ResponseReturnValue:
    return redirect(url_for('core.feed'))


@core.route('/feed/')
@login_required
def feed() -> ResponseReturnValue:
    posts = list(Post.query.order_by(sa.desc(Post.timestamp)))
    for post in posts:
        post.liked = True if current_user.id in [
            like.user_id for like in post.likes] else False
    return render_template('core/feed.html', posts=posts, feed_title='Feed')


@core.route('/newest/')
@login_required
def newest() -> ResponseReturnValue:
    posts = list(Post.query.order_by(sa.desc(Post.timestamp)))
    for post in posts:
        post.liked = True if current_user.id in [
            like.user_id for like in post.likes] else False
    return render_template('core/feed.html', posts=posts, feed_title='Newest posts')


@core.route('/search/')
@login_required
def search() -> ResponseReturnValue:
    return render_template('core/search.html')


@core.route('/post/', methods=['POST'])
@login_required
def post() -> ResponseReturnValue:
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(user_id=current_user.id,
                    post=post_form.post.data)
        db.session.add(post)
        db.session.commit()

    elif post_form.errors:
        for field, errors in post_form.errors.items():
            for error in errors:
                flash(f'{field.capitalize()}: {error}', category='danger')

    next_page = request.referrer
    if next_page is not None and is_safe_url(next_page, {request.host}):
        return redirect(next_page)
    return redirect(url_for('.feed'))


@core.route('/profile/<username>')
@login_required
def profile(username: str) -> ResponseReturnValue:
    profile_form = EditProfileForm()
    user = User.query.filter_by(username=username).first_or_404()
    profile_form.bio.data = user.bio
    posts = Post.query.filter_by(
        user_id=user.id).order_by(sa.desc(Post.timestamp))

    return render_template('core/profile.html', user=user, posts=posts, profile_form=profile_form)


@core.route('/profile/edit/', methods=['POST'])
def edit_profile() -> ResponseReturnValue:
    profile_form = EditProfileForm()
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

    return redirect(url_for('.profile', username=current_user.username))


@core.route('/serve/pfp/<username>')
@login_required
def profile_pic(username: str) -> ResponseReturnValue:
    user = User.query.filter_by(username=username).first_or_404()
    img_name = secure_filename(f'{user.id}_pfp.webp')
    img_path = profile_imgs.path(img_name)

    if path.exists(img_path):
        return send_file(img_path)
    return send_from_directory('static', 'images/default_pfp.webp')
