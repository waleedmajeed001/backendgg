from flask import Blueprint
from controllers.todo_controller import TodoController

todo_bp = Blueprint('todos', __name__, url_prefix='/api/todos')

@todo_bp.route('/<todo_id>/toggle', methods=['PATCH'])
def toggle_todo(todo_id):
    """PATCH /api/todos/:id/toggle - Toggle todo completion"""
    return TodoController.toggle_todo(todo_id)

@todo_bp.route('/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    """GET /api/todos/:id - Get a specific todo"""
    return TodoController.get_todo(todo_id)

@todo_bp.route('/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """PUT /api/todos/:id - Update a todo"""
    return TodoController.update_todo(todo_id)

@todo_bp.route('/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """DELETE /api/todos/:id - Delete a specific todo"""
    return TodoController.delete_todo(todo_id)

@todo_bp.route('/', methods=['GET'])
def get_all_todos():
    """GET /api/todos - Get all todos"""
    return TodoController.get_all_todos()

@todo_bp.route('/', methods=['POST'])
def create_todo():
    """POST /api/todos - Create a new todo"""
    return TodoController.create_todo()

@todo_bp.route('/', methods=['DELETE'])
def delete_all_todos():
    """DELETE /api/todos - Delete all todos"""
    return TodoController.delete_all_todos() 