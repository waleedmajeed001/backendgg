from flask import request, jsonify
from typing import Dict, Any
from services.todo_service import todo_service

class TodoController:
    
    @staticmethod
    def get_all_todos() -> tuple[Dict[str, Any], int]:
        """GET /api/todos - Retrieve all todos"""
        try:
            todos = todo_service.get_all_todos()
            return jsonify(todos), 200
        except Exception as error:
            return jsonify({'error': 'Failed to fetch todos'}), 500
    
    @staticmethod
    def get_todo(todo_id: str) -> tuple[Dict[str, Any], int]:
        """GET /api/todos/:id - Retrieve a single todo by ID"""
        try:
            todo = todo_service.get_todo_by_id(todo_id)
            if not todo:
                return jsonify({'error': 'Todo not found'}), 404
            return jsonify(todo), 200
        except Exception as error:
            return jsonify({'error': 'Failed to fetch todo'}), 500
    
    @staticmethod
    def create_todo() -> tuple[Dict[str, Any], int]:
        """POST /api/todos - Create a new todo"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            text = data.get('text')
            color = data.get('color')
            
            if not text or not text.strip():
                return jsonify({'error': 'Text is required'}), 400
            
            new_todo = todo_service.create_todo(text, color)
            return jsonify(new_todo), 201
        except ValueError as error:
            return jsonify({'error': str(error)}), 400
        except Exception as error:
            return jsonify({'error': 'Failed to create todo'}), 500
    
    @staticmethod
    def update_todo(todo_id: str) -> tuple[Dict[str, Any], int]:
        """PUT /api/todos/:id - Update an existing todo"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            text = data.get('text')
            completed = data.get('completed')
            color = data.get('color')
            
            updated_todo = todo_service.update_todo(todo_id, text, completed, color)
            if not updated_todo:
                return jsonify({'error': 'Todo not found'}), 404
            
            return jsonify(updated_todo), 200
        except Exception as error:
            return jsonify({'error': 'Failed to update todo'}), 500
    
    @staticmethod
    def toggle_todo(todo_id: str) -> tuple[Dict[str, Any], int]:
        """PATCH /api/todos/:id/toggle - Toggle todo completion status"""
        try:
            updated_todo = todo_service.toggle_todo(todo_id)
            if not updated_todo:
                return jsonify({'error': 'Todo not found'}), 404
            
            return jsonify(updated_todo), 200
        except Exception as error:
            return jsonify({'error': 'Failed to toggle todo'}), 500
    
    @staticmethod
    def delete_todo(todo_id: str) -> tuple[Dict[str, Any], int]:
        """DELETE /api/todos/:id - Delete a specific todo"""
        try:
            deleted_todo = todo_service.delete_todo(todo_id)
            if not deleted_todo:
                return jsonify({'error': 'Todo not found'}), 404
            
            return jsonify({
                'message': 'Todo deleted successfully',
                'deletedTodo': deleted_todo
            }), 200
        except Exception as error:
            return jsonify({'error': 'Failed to delete todo'}), 500
    
    @staticmethod
    def delete_all_todos() -> tuple[Dict[str, Any], int]:
        """DELETE /api/todos - Delete all todos"""
        try:
            deleted_count = todo_service.delete_all_todos()
            return jsonify({
                'message': 'All todos deleted successfully',
                'deletedCount': deleted_count
            }), 200
        except Exception as error:
            return jsonify({'error': 'Failed to delete all todos'}), 500
    
    @staticmethod
    def health_check() -> tuple[Dict[str, Any], int]:
        """GET /api/health - Health check endpoint"""
        from datetime import datetime
        return jsonify({
            'status': 'OK',
            'message': 'Todo API is running',
            'timestamp': datetime.now().isoformat(),
            'todoCount': todo_service.get_todo_count()
        }), 200 
    @staticmethod
    def get_completed_todos() -> tuple[Dict[str, Any], int]:
        """GET /api/todos/completed - Retrieve all completed todos"""
        try:
            completed_todos = todo_service.get_completed_todos()
            return jsonify(completed_todos), 200
        except Exception as e:
            return jsonify({"error": "Failed to fetch completed todos"}), 500
        