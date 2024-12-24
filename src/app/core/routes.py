from os import path

from flask import (abort, flash, redirect, render_template, send_file,
                   send_from_directory, url_for)
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required

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


@core.route('/profile/<username>', methods=['POST', 'GET'])
@login_required
def profile(username: str) -> ResponseReturnValue:
    if username == current_user.username:
        form = EditProfileForm()
        if form.validate_on_submit():
            current_user.bio = form.bio.data
            db.session.add(current_user)
            db.session.commit()
            
            img = optimize_img(form.profile_img.data)
            name = f'{current_user.id}_pfp.'
            profile_imgs.save(img, name=name) # type: ignore
            flash('Profile information updated!', category='success')
        return render_template('core/user_profile.html', form=form)

    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('core/profile.html', user=user)


@core.route('/serve/pfp/<username>')
@login_required
def profile_pic(username: str) -> ResponseReturnValue:
    user = User.query.filter_by(username = username).first()
    img_path = profile_imgs.path(f'{user.id}_pfp.webp')
    
    if user is not None and path.exists(img_path):
        return send_file(img_path)
    return send_from_directory('static', 'images/default_pfp.webp')
    