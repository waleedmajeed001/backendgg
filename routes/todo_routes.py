from flask import Blueprint, request, jsonify
from controllers.todo_controller import TodoController

todo_bp = Blueprint('todos', __name__, url_prefix='/api/todos')

def get_user_id_from_request():
    """Extract user_id from request headers or query params"""
    # Check for user_id in headers (for authenticated requests)
    user_id = request.headers.get('X-User-ID')
    if user_id:
        return user_id
    
    # For guest users, return None
    return None

@todo_bp.route('/completed', methods=['GET'])
def get_completed_todos():
    """GET /api/todos/completed - Get all completed todos"""
    user_id = get_user_id_from_request()
    return TodoController.get_completed_todos(user_id)

@todo_bp.route('/<todo_id>/toggle', methods=['PATCH'])
def toggle_todo(todo_id):
    """PATCH /api/todos/:id/toggle - Toggle todo completion"""
    user_id = get_user_id_from_request()
    return TodoController.toggle_todo(todo_id, user_id)

@todo_bp.route('/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    """GET /api/todos/:id - Get a specific todo"""
    user_id = get_user_id_from_request()
    return TodoController.get_todo(todo_id, user_id)

@todo_bp.route('/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """PUT /api/todos/:id - Update a todo"""
    user_id = get_user_id_from_request()
    return TodoController.update_todo(todo_id, user_id)

@todo_bp.route('/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """DELETE /api/todos/:id - Delete a specific todo"""
    user_id = get_user_id_from_request()
    return TodoController.delete_todo(todo_id, user_id)

@todo_bp.route('/', methods=['GET'])
def get_all_todos():
    """GET /api/todos - Get all todos"""
    user_id = get_user_id_from_request()
    return TodoController.get_all_todos(user_id)

@todo_bp.route('/', methods=['POST'])
def create_todo():
    """POST /api/todos - Create a new todo"""
    user_id = get_user_id_from_request()
    return TodoController.create_todo(user_id)

@todo_bp.route('/guest-count', methods=['GET'])
def get_guest_todo_count():
    """GET /api/todos/guest-count - Get guest todo count"""
    return TodoController.get_guest_todo_count()

@todo_bp.route('/', methods=['DELETE'])
def delete_all_todos():
    """DELETE /api/todos - Delete all todos"""
    user_id = get_user_id_from_request()
    return TodoController.delete_all_todos(user_id) 