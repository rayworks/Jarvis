from datetime import timedelta

from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user, login_required

from app import get_app, login_manager
from app.forms import LoginForm
from app.model import User

login = Blueprint('login', __name__)


@login.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html', login_url=url_for('login.index'), register_url=url_for('register.index'))
    else:
        return login_validate()


def login_validate():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    remember = request.json.get('remember', False)
    form = LoginForm()
    valid = form.validate()
    print(form.errors)
    if valid:
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(pwd=password):
            login_user(user, remember)
            session.permanent = True
            app = get_app()
            app.permanent_session_lifetime = timedelta(minutes=app.config['SESSION_LIFETIME'])
            return jsonify({'next_url': url_for('todo_list.index')})
        else:
            flash('Invalid username or password, please try again.')
    return jsonify({'next_url': url_for('login.index')})


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@login.route('/logout', methods=['GET'])
@login_required
def logout():
    flash('You were logged out')
    logout_user()
    return redirect(url_for('login.index'))
