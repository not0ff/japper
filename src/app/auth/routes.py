from flask import render_template, redirect, url_for, session, request
from . import auth


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['logged'] = True

        return redirect(url_for('core.index'))
    else:
        return render_template('auth/login.html')


@auth.route('/logout/')
def logout():
    session.clear()

    return redirect(url_for('core.index'))
