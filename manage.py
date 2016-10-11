#!/usr/bin/env python
import os
from app import create_app, db
from app.forms import LoginForm
# from app.models import User, Role, Permission, Post
from flask import Flask, request, jsonify
from flask import make_response
from flask import abort
from flask import render_template
from flask import flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission,
                Post=Post)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html'), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        if form.username.data != 'user' or form.password.data != 'pass':
            flash('Invalid username or password, please try again.')
        else:
            flash('login successfully')
    return render_template('login.html', form=form)


if __name__ == '__main__':
    manager.run()
