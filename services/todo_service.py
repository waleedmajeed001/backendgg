import uuid
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from database import get_database

class TodoService:
    def __init__(self):
        pass
    
    def get_all_todos(self) -> List[Dict]:
        db = get_database()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        todos_list = []
        for row in rows:
            todos_list.append({
                'id': row[0],
                'text': row[1],
                'color': row[2],
                'completed': bool(row[3]),
                'createdAt': row[4],
                'updatedAt': row[5]
            })
        db.close()
        return todos_list
    
    def get_completed_todos(self) -> List[Dict]:
        db = get_database()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM todos WHERE completed = 1 ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        todos_list = []
        for row in rows:
            todos_list.append({
                'id': row[0],
                'text': row[1],
                'color': row[2],
                'completed': bool(row[3]),
                'createdAt': row[4],
                'updatedAt': row[5]
            })
        db.close()
        return todos_list
    
    def get_todo_by_id(self, todo_id: str) -> Optional[Dict]:
        db = get_database()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        
        if row:
            result = {
                'id': row[0],
                'text': row[1],
                'color': row[2],
                'completed': bool(row[3]),
                'createdAt': row[4],
                'updatedAt': row[5]
            }
            db.close()
            return result
        db.close()
        return None
    
    def create_todo(self, text: str, color: Optional[str] = None) -> Dict:
        if not text or not text.strip():
            raise ValueError("Text is required")
        
        todo_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        db = get_database()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO todos (id, text, color, completed, created_at) VALUES (?, ?, ?, ?, ?)",
            (todo_id, text.strip(), color, False, created_at)
        )
        db.commit()
        db.close()
        
        return {
            'id': todo_id,
            'text': text.strip(),
            'color': color,
            'completed': False,
            'createdAt': created_at
        }
    
    def update_todo(self, todo_id: str, text: Optional[str] = None, 
                   completed: Optional[bool] = None, color: Optional[str] = None) -> Optional[Dict]:
        existing_todo = self.get_todo_by_id(todo_id)
        if not existing_todo:
            return None
        
        update_fields = []
        update_values = []
        
        if text is not None:
            update_fields.append("text = ?")
            update_values.append(text.strip())
        if completed is not None:
            update_fields.append("completed = ?")
            update_values.append(completed)
        if color is not None:
            update_fields.append("color = ?")
            update_values.append(color)
        
        if not update_fields:
            return existing_todo
        
        update_fields.append("updated_at = ?")
        update_values.append(datetime.now().isoformat())
        update_values.append(todo_id)
        
        db = get_database()
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?",
            update_values
        )
        db.commit()
        db.close()
        
        return self.get_todo_by_id(todo_id)
    
    def toggle_todo(self, todo_id: str) -> Optional[Dict]:
        existing_todo = self.get_todo_by_id(todo_id)
        if not existing_todo:
            return None
        
        new_completed = not existing_todo['completed']
        updated_at = datetime.now().isoformat()
        
        db = get_database()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE todos SET completed = ?, updated_at = ? WHERE id = ?",
            (new_completed, updated_at, todo_id)
        )
        db.commit()
        db.close()
        
        return self.get_todo_by_id(todo_id)
    
    def delete_todo(self, todo_id: str) -> Optional[Dict]:
        existing_todo = self.get_todo_by_id(todo_id)
        if not existing_todo:
            return None
        
        db = get_database()
        cursor = db.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        db.commit()
        db.close()
        
        return existing_todo
    
    def delete_all_todos(self) -> int:
        db = get_database()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM todos")
        count = cursor.fetchone()[0]
        
        cursor.execute("DELETE FROM todos")
        db.commit()
        db.close()
        
        return count
    
    def get_todo_count(self) -> int:
        db = get_database()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM todos")
        count = cursor.fetchone()[0]
        db.close()
        return count

todo_service = TodoService() 