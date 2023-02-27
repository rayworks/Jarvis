#!/usr/bin/env python
import os

from flask import make_response, jsonify
from flask import render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.model import Todo, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app'))

print(app_dir)

with app.app_context():
    db.create_all()

def make_shell_context():
    return dict(app=app, db=db, Todo=Todo, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.route('/test', methods=['GET'])
def test_html():
    return render_template('test.html'), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo-list', methods=['GET'])
def get_all_todo():
    items = Todo.query.all()

    json_array = []
    for i in items:
        json_array.append({"item": i.title})

    return jsonify({"items": json_array})


if __name__ == '__main__':
    manager.run()
