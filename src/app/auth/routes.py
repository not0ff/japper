from flask import render_template, redirect, url_for, session, request
from app.forms import LoginForm, SignupForm
from . import auth


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['logged'] = True
        return redirect(url_for('core.index'))
    return render_template('auth/login.html', form=form)

@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        session['logged'] = True
        return redirect(url_for('core.index'))
    return render_template('auth/signup.html', form=form)



@auth.route('/logout/')
def logout():
    session.clear()

    return redirect(url_for('core.index'))
