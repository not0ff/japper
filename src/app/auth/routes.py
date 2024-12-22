from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url
from app import db
from app.forms import LoginForm, SignupForm
from app.models import User
from . import auth


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password!', category='danger')
            return redirect(url_for('.login', **request.args))

        login_user(user)
        next_page = request.args.get('next')
        if next_page is not None and is_safe_url(next_page, {request.root_url}):
            return redirect(next_page)

        return redirect(url_for('core.index'))

    return render_template('auth/login.html', form=form)


@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Registration completed! You can now log into your account',
              category='success')
        return redirect(url_for('.login'))

    return render_template('auth/signup.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))
