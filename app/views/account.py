from flask import Blueprint, flash, jsonify, render_template, request, url_for

from app.forms import RegisterForm
from app.model import User, db

register = Blueprint('register', __name__)


@register.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template(
            'register.html', login_url=url_for('login.index'), register_url=url_for('register.index'))
    else:
        return register_validate()


def register_validate():
    form = RegisterForm()
    if form.validate_on_submit():
        input_username = request.json.get('username', None)
        input_password = request.json.get('password', None)
        input_email = request.json.get('email', None)
        user = User.query.filter_by(username=input_username).first()
        if user is not None:
            flash('User {} has been registered, please change it.'.format(input_username))
        elif User.query.filter_by(email=input_email).first() is not None:
            flash('Email {} has been registered, please change it.'.format(input_email))
        else:
            flash('Success to register, please enjoy your journey!')
            db.session.add(User(username=input_username, password=input_password, email=input_email))
            db.session.commit()
            return jsonify({'next_url': url_for('login.index')})
    return jsonify({'next_url': url_for('register.index')})
