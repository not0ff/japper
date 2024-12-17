from flask import render_template, redirect, url_for
from . import core

@core.route('/')
def index():
    return redirect(url_for('core.feed'))

@core.route('/feed/')
def feed():
    return render_template('core/feed.html')

@core.route('/newest/')
def newest():
    return render_template('core/newest.html')

@core.route('/search/')
def search():
    return render_template('core/search.html')

@core.route('/profile/')
def profile():
    return render_template('core/profile.html')