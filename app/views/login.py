from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user, LoginManager, login_required

from app import login_manager
from app.forms import LoginForm
from app.model import User

login = Blueprint('login', __name__)


@login.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(pwd=form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('todo_list.index'))
        flash('Invalid username or password, please try again.')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@login.route('/logout', methods=['GET'])
@login_required
def logout():
    flash('You were logged out')
    logout_user()
    return redirect(url_for('login.index'))
