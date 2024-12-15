from flask import render_template
from . import core

@core.route('/')
def index():
    return render_template('core/home.html')