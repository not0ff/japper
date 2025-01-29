import sqlalchemy as sa
from flask import redirect, render_template, url_for
from flask.typing import ResponseReturnValue
from flask_login import login_required

from app.forms import SearchPostForm
from app.models import Post
from app.utils import get_feed, search_post

from . import core


@core.route('/null', methods=['POST', 'GET'])
def null() -> ResponseReturnValue:
    return 'Invalid attribute for requested endpoint'


@core.route('/')
def index() -> ResponseReturnValue:
    return redirect(url_for('core.feed'))


@core.route('/feed/')
@login_required
def feed() -> ResponseReturnValue:
    posts = get_feed()
    return render_template('core/feed.html', posts=posts, feed_title='Feed')


@core.route('/newest/')
@login_required
def newest() -> ResponseReturnValue:
    posts = Post.query.order_by(sa.desc(Post.timestamp))
    return render_template('core/feed.html', posts=posts, feed_title='Newest posts')


@core.route('/search/', methods=['POST', 'GET'])
@login_required
def search() -> ResponseReturnValue:
    search_form = SearchPostForm()

    posts = None
    if search_form.validate_on_submit():
        posts = search_post(search_form.query.data)

    return render_template('core/search.html', search_form=search_form, posts=posts)
