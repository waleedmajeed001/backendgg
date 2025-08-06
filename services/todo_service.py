import uuid
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class TodoService:
    def __init__(self):
        self.todos: List[Dict] = []
    
    def get_all_todos(self) -> List[Dict]:
        """Get all todos"""
        return self.todos.copy()
    
    def get_todo_by_id(self, todo_id: str) -> Optional[Dict]:
        """Get a specific todo by ID"""
        return next((todo for todo in self.todos if todo['id'] == todo_id), None)
    
    def create_todo(self, text: str, color: Optional[str] = None) -> Dict:
        """Create a new todo"""
        if not text or not text.strip():
            raise ValueError("Text is required")
        
        new_todo = {
            'id': str(uuid.uuid4()),
            'text': text.strip(),
            'color': color,
            'completed': False,
            'createdAt': datetime.now().isoformat()
        }
        
        self.todos.append(new_todo)
        return new_todo
    
    def update_todo(self, todo_id: str, text: Optional[str] = None, 
                   completed: Optional[bool] = None, color: Optional[str] = None) -> Optional[Dict]:
        """Update an existing todo"""
        todo_index = self._find_todo_index(todo_id)
        if todo_index == -1:
            return None
        
        updated_todo = self.todos[todo_index].copy()
        
        if text is not None:
            updated_todo['text'] = text.strip()
        if completed is not None:
            updated_todo['completed'] = completed
        if color is not None:
            updated_todo['color'] = color
        
        updated_todo['updatedAt'] = datetime.now().isoformat()
        self.todos[todo_index] = updated_todo
        
        return updated_todo
    
    def toggle_todo(self, todo_id: str) -> Optional[Dict]:
        """Toggle todo completion status"""
        todo_index = self._find_todo_index(todo_id)
        if todo_index == -1:
            return None
        
        self.todos[todo_index]['completed'] = not self.todos[todo_index]['completed']
        self.todos[todo_index]['updatedAt'] = datetime.now().isoformat()
        
        return self.todos[todo_index]
    
    def delete_todo(self, todo_id: str) -> Optional[Dict]:
        """Delete a specific todo"""
        todo_index = self._find_todo_index(todo_id)
        if todo_index == -1:
            return None
        
        deleted_todo = self.todos.pop(todo_index)
        return deleted_todo
    
    def delete_all_todos(self) -> int:
        """Delete all todos and return count"""
        deleted_count = len(self.todos)
        self.todos.clear()
        return deleted_count
    
    def get_todo_count(self) -> int:
        """Get total number of todos"""
        return len(self.todos)
    
    def _find_todo_index(self, todo_id: str) -> int:
        """Find the index of a todo by ID"""
        for i, todo in enumerate(self.todos):
            if todo['id'] == todo_id:
                return i
        return -1


todo_service = TodoService() 