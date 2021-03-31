from flask import jsonify

from app.api_1_0 import api
from app.model import Todo


@api.route('/todo-list', methods=['GET'])
def get_all_todo():
    """
    Simply retrieves all the ToDo items [For testing usage only].
    You may test with path: /api/v1.0/todo-list
    """
    items = Todo.query.all()

    json_array = []
    for i in items:
        json_array.append({"item": i.title})

    return jsonify({"items": json_array})
