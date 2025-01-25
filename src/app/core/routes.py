from os import path
from typing import Sequence, Optional

import sqlalchemy as sa
from flask import (redirect, render_template, send_file, send_from_directory,
                   url_for)
from flask.typing import ResponseReturnValue
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.extensions import profile_imgs
from app.forms import EditProfileForm, SearchPostForm, FollowProfileForm
from app.models import Post, User
from app.utils import get_feed, search_post

from . import core


@core.route('/')
def index() -> ResponseReturnValue:
    return redirect(url_for('core.feed'))


@core.route('/feed/')
@login_required
def feed() -> ResponseReturnValue:
    posts: Sequence[Post] = get_feed()
    return render_template('core/feed.html', posts=posts, feed_title='Feed')


@core.route('/newest/')
@login_required
def newest() -> ResponseReturnValue:
    posts: Sequence[Post] = Post.query.order_by(sa.desc(Post.timestamp))
    return render_template('core/feed.html', posts=posts, feed_title='Newest posts')


@core.route('/search/', methods=['POST', 'GET'])
@login_required
def search() -> ResponseReturnValue:
    search_form = SearchPostForm()
    
    posts: Optional[Sequence[Post]] = None
    if search_form.validate_on_submit():
        posts = search_post(search_form.query.data)

    return render_template('core/search.html', search_form=search_form, posts=posts)


@core.route('/profile/<username>')
@login_required
def profile(username: str) -> ResponseReturnValue:
    profile_form: EditProfileForm = EditProfileForm()
    follow_profile_form: FollowProfileForm = FollowProfileForm()
    user: User = User.query.filter_by(username=username).first_or_404()
    posts: Sequence[Post] = Post.query.filter_by(
        user_id=user.id).order_by(sa.desc(Post.timestamp))
    
    profile_form.bio.data = user.bio
    return render_template('core/profile.html', user=user, posts=posts, profile_form=profile_form, follow_profile_form=follow_profile_form)


@core.route('/serve/pfp/<username>')
@login_required
def profile_pic(username: str) -> ResponseReturnValue:
    user: User = User.query.filter_by(username=username).first_or_404()
    img_name = secure_filename(f'{user.id}_pfp.webp')
    img_path = profile_imgs.path(img_name)

    if path.exists(img_path):
        return send_file(img_path)
    return send_from_directory('static', 'images/default_pfp.webp')
