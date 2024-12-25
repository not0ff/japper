from flask import flash, redirect, render_template, request, session, url_for
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required, login_user, logout_user
from is_safe_url import is_safe_url

from app import db
from app.forms import LoginForm, SignupForm
from app.models import User

from . import auth


@auth.route('/login/', methods=['GET', 'POST'])
def login() -> ResponseReturnValue:
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password!', category='danger')
            return redirect(url_for('.login'))
        login_user(user, remember=login_form.remember.data)
        
        next_page = session.pop('next', None)
        if next_page is not None and is_safe_url(next_page, {request.host}):
            return redirect(next_page)
        
        return redirect(url_for('core.index'))
    return render_template('auth/login.html', login_form=login_form)


@auth.route('/signup/', methods=['GET', 'POST'])
def signup() -> ResponseReturnValue:
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        user = User(username=signup_form.username.data)
        user.set_password(signup_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration completed! You can now log into your account',
              category='success')
        return redirect(url_for('.login'))
    return render_template('auth/signup.html', signup_form=signup_form)


@auth.route('/logout/')
@login_required
def logout() -> ResponseReturnValue:
    logout_user()
    return redirect(url_for('.login'))
