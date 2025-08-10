from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/api/user')
user_service = UserService()

@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not all([email, password, name]):
            return jsonify({'error': 'Email, password, and name are required'}), 400
        
        success, message, user_data = user_service.register_user(email, password, name)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'data': user_data
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 400
            
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'error': 'Email and password are required'}), 400
        
        success, message, user_data = user_service.login_user(email, password)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'data': user_data
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 401
            
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@user_bp.route('/guest-todo-count', methods=['GET'])
def get_guest_todo_count():
    """Get count of guest todos"""
    try:
        count = user_service.get_guest_todo_count()
        return jsonify({
            'success': True,
            'data': {
                'count': count,
                'remaining': max(0, 3 - count)
            }
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get guest todo count: {str(e)}'}), 500
