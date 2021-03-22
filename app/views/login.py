from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.forms import LoginForm

login = Blueprint('login', __name__)


@login.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():

        if form.username.data != 'user' or form.password.data != 'pass':
            flash('Invalid username or password, please try again.')
        else:
            flash('login successfully')
            session['logged_in'] = True
            return redirect(url_for('todos'))
    return render_template('login.html', form=form)


@login.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login.index'))
