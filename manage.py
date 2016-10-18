#!/usr/bin/env python
import os
from app import create_app, db
from app.forms import LoginForm
# from app.models import User, Role, Permission, Post
from flask import Flask, request, jsonify
from flask import abort
from flask import render_template
from flask import flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

from flask.ext.wtf import Form
from wtforms import ValidationError

from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

from sqlite3 import dbapi2 as sqlite3
from flask import request, session, g, redirect, url_for

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission,
                Post=Post)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

db_path = 'dev.db'


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
            session['logged_in'] = True
            # items = ['list item 1', 'list item 2', 'list item 3', 'list item 4']
            return redirect(url_for('todos'))
    return render_template('login.html', form=form)


def init_db():
    """ init the database."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    with app.open_resource('./app/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    return g.sqlite_db


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def connect_db():
    db_file = db_path  ##app.config['SQLALCHEMY_DATABASE_URI']
    print db_file
    db = sqlite3.connect(db_file)
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/add', methods=['POST'])
def add_item():
    if not session['logged_in']:
        abort(401)
    db = get_db()
    db.execute('insert into todo (title)  values(?)', [request.form['title']])
    db.commit()

    flash('new entry added successfully')
    return redirect(url_for('todos'))


@app.route('/del/<int:id>', methods=['POST'])
def del_item(id):
    print "delete item ", id

    db = get_db()
    # http://stackoverflow.com/questions/3977570/how-to-delete-record-from-table
    db.execute('delete from todo where id = ?', (id,))
    db.commit()
    return redirect(url_for('todos'))


@app.route('/')
def todos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.execute('select * from todo order by id desc')
    items = cursor.fetchall()

    return render_template('todo_list.html', entries=items)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


if __name__ == '__main__':
    manager.run()
