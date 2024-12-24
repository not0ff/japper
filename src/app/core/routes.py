from os import path, remove

from flask import (abort, flash, redirect, render_template, send_file,
                   send_from_directory, url_for)
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.extensions import db, profile_imgs
from app.forms import EditProfileForm
from app.models import User
from app.utils import optimize_img

from . import core


@core.route('/')
def index() -> ResponseReturnValue:
    return redirect(url_for('core.feed'))


@core.route('/feed/')
@login_required
def feed() -> ResponseReturnValue:
    return render_template('core/feed.html')


@core.route('/newest/')
@login_required
def newest() -> ResponseReturnValue:
    return render_template('core/newest.html')


@core.route('/search/')
@login_required
def search() -> ResponseReturnValue:
    return render_template('core/search.html')


@core.route('/profile/<username>')
@login_required
def profile(username: str) -> ResponseReturnValue:
    if username == current_user.username:
        form = EditProfileForm()
        form.bio.data = current_user.bio
        return render_template('core/user_profile.html', form=form)

    user = User.query.filter_by(username=username).first_or_404()
    return render_template('core/profile.html', user=user)


@core.route('/profile/edit/', methods=['POST'])
def edit_profile() -> ResponseReturnValue:
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.bio.data != current_user.bio and form.bio.data:
            current_user.bio = form.bio.data
            db.session.add(current_user)
            db.session.commit()
            flash('Profile bio changed', category='success')

        if form.profile_img.data:
            img = optimize_img(form.profile_img.data)
            name = secure_filename(f'{current_user.id}_pfp.webp')

            if path.exists(img_path := profile_imgs.path(name)):
                remove(img_path)

            profile_imgs.save(img, name=name)  # type: ignore
            flash('Profile picture updated!', category='success')
    
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
