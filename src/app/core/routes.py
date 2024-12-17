from flask import render_template, redirect, url_for
from . import core
from app.utils import login_required


@core.route('/')
def index():
    return redirect(url_for('core.feed'))


@core.route('/feed/')
@login_required
def feed():
    return render_template('core/feed.html')


@core.route('/newest/')
@login_required
def newest():
    return render_template('core/newest.html')


@core.route('/search/')
@login_required
def search():
    return render_template('core/search.html')


@core.route('/profile/')
@login_required
def profile():
    return render_template('core/profile.html')
