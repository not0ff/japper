from flask import redirect, render_template, url_for
from flask.typing import ResponseReturnValue
from flask_login import login_required

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


@core.route('/profile/')
@login_required
def profile() -> ResponseReturnValue:
    return render_template('core/profile.html')
