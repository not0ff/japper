from flask import redirect, url_for, session
from functools import wraps


def is_logged():
    if session.get('logged') is None:
        return False
    else:
        return True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged():
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
