from flask import render_template, request, flash, url_for
from app.utils import redirect_to_referrer


def bad_request(err):
    return render_template('errors/default.html', status=400, message='Bad request submitted'), 400


def unauthorized(err):
    return render_template('errors/default.html', status=401, message='You are unauthorized to access this page'), 401

def forbidden(err):
    return render_template('errors/default.html', status=403, message='Access forbidden'), 403


def not_found(err):
    if request.path.startswith('/profile/'):
        return render_template('errors/profile_404.html'), 404
    return render_template('errors/default.html', status=404, message='Page not found'), 404


def method_not_allowed(err):
    return render_template('errors/default.html', status=405, message='Method not allowed'), 405


def payload_too_large(err):
    if request.path.startswith('/profile/edit'):
        flash('Too large payload submitted!', category='danger')
        return redirect_to_referrer()
    
    return render_template('errors/default.html', status=413, message='Request payload is too large'), 413


def internal_error(err):
    return render_template('errors/default.html', status=500, message='Internal server error'), 500
