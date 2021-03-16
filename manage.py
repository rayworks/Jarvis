#!/usr/bin/env python
import os
from datetime import datetime

from flask import abort
from flask import flash
from flask import make_response, jsonify
from flask import render_template
from flask import request, session, redirect, url_for
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.forms import LoginForm
from app.model import Todo

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Todo=Todo)


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
            session['logged_in'] = True
            return redirect(url_for('todos'))
    return render_template('login.html', form=form)


@app.route('/add', methods=['POST'])
def add_item():
    if not session['logged_in']:
        abort(401)

    td = Todo(request.form['title'])
    db.session.add(td)
    db.session.commit()

    flash('new entry added successfully')
    return redirect(url_for('todos'))


@app.route('/del/<int:id>', methods=['POST'])
def del_item(id):
    print "delete item ", id

    td = Todo.query.filter_by(id=id).first()
    db.session.delete(td)
    db.session.commit()

    return redirect(url_for('todos'))


@app.route('/')
def todos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    items = Todo.query.all()
    return render_template('todo_list.html', entries=items, current_time=datetime.utcnow())


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo-list', methods=['GET'])
def get_all_todo():
    items = Todo.query.all()

    json_array = []
    for i in items:
        json_array.append({"item" : i.title})

    return jsonify({"items": json_array})


if __name__ == '__main__':
    manager.run()
