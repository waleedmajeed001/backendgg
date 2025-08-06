from flask import Blueprint
from controllers.todo_controller import TodoController

health_bp = Blueprint('health', __name__, url_prefix='/api')

@health_bp.route('/health', methods=['GET'])
def health_check():
    """GET /api/health - Health check endpoint"""
    return TodoController.health_check() 