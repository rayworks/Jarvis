from flask import Blueprint, flash, redirect, render_template, url_for

from app.forms import RegisterForm
from app.model import User, db

register = Blueprint('register', __name__)


@register.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterForm()
    input_username = form.username.data
    input_password = form.password.data
    input_email = form.email.data
    if form.validate_on_submit():
        user = User.query.filter_by(username=input_username).first()
        if user is not None:
            flash('User {} has been registered, please change it.'.format(input_username))
        elif User.query.filter_by(email=input_email).first() is not None:
            flash('Email {} has been registered, please change it.'.format(input_email))
        else:
            flash('Success to register, please enjoy your journey!')
            db.session.add(User(username=input_username, password=input_password, email=input_email))
            db.session.commit()
            return redirect(url_for('login.index'))
    return render_template('register.html', form=form)
