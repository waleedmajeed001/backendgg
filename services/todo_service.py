import sqlite3
import uuid
import datetime
from typing import List, Dict, Optional
from database import get_db_connection, DATABASE_URL
from services.user_service import UserService

class TodoService:
    def __init__(self):
        self.db_path = 'todo_app.db'
        self.user_service = UserService()
        
    def _get_param_placeholder(self, index: int) -> str:
        """Get the correct parameter placeholder based on database type"""
        if DATABASE_URL.startswith('postgresql://'):
            return f'%s'  # PostgreSQL uses %s
        else:
            return '?'    # SQLite uses ?

    def _generate_id(self) -> str:
        """Generate unique todo ID"""
        return str(uuid.uuid4())

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.datetime.now().isoformat()

    def get_all_todos(self, user_id: Optional[str] = None) -> List[Dict]:
        """Get all todos for a user or guest todos if no user_id"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if user_id:
                cursor.execute("""
                    SELECT id, user_id, text, color, completed, created_at, updated_at
                    FROM todos WHERE user_id = %s
                    ORDER BY created_at DESC
                """, (user_id,))
            else:
                cursor.execute("""
                    SELECT id, user_id, text, color, completed, created_at, updated_at
                    FROM todos WHERE user_id IS NULL
                    ORDER BY created_at DESC
                """)

            todos = cursor.fetchall()
            conn.close()

            return [self._to_dict(todo) for todo in todos]

        except Exception as e:
            return []

    def get_todo_by_id(self, todo_id: str, user_id: Optional[str] = None) -> Optional[Dict]:
        """Get todo by ID, ensuring user can only access their own todos"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if user_id:
                cursor.execute("""
                    SELECT id, user_id, text, color, completed, created_at, updated_at
                    FROM todos WHERE id = %s AND user_id = %s
                """, (todo_id, user_id))
            else:
                cursor.execute("""
                    SELECT id, user_id, text, color, completed, created_at, updated_at
                    FROM todos WHERE id = %s AND user_id IS NULL
                """, (todo_id,))

            todo = cursor.fetchone()
            conn.close()

            return self._to_dict(todo) if todo else None

        except Exception as e:
            return None

    def create_todo(self, text: str, user_id: Optional[str] = None, color: Optional[str] = None) -> Optional[Dict]:
        """Create a new todo"""
        try:
            if not text or not text.strip():
                raise ValueError("Text is required")

            # Check guest todo limit
            if not user_id:
                guest_count = self.user_service.get_guest_todo_count()
                if guest_count >= 3:
                    raise ValueError("Guest users can only create 3 todos. Please register to create unlimited todos.")

            conn = get_db_connection()
            cursor = conn.cursor()

            todo_id = self._generate_id()
            created_at = self._get_current_timestamp()

            cursor.execute("""
                INSERT INTO todos (id, user_id, text, color, completed, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (todo_id, user_id, text.strip(), color, False, created_at, created_at))

            conn.commit()
            conn.close()

            return {
                'id': todo_id,
                'user_id': user_id,
                'text': text.strip(),
                'color': color,
                'completed': False,
                'createdAt': created_at,
                'updatedAt': created_at
            }

        except Exception as e:
            raise e

    def update_todo(self, todo_id: str, text: Optional[str] = None, completed: Optional[bool] = None, 
                   color: Optional[str] = None, user_id: Optional[str] = None) -> Optional[Dict]:
        """Update a todo"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if todo exists and user has permission
            if user_id:
                cursor.execute("SELECT id FROM todos WHERE id = %s AND user_id = %s", (todo_id, user_id))
            else:
                cursor.execute("SELECT id FROM todos WHERE id = %s AND user_id IS NULL", (todo_id,))

            if not cursor.fetchone():
                conn.close()
                return None

            # Build update query
            updates = []
            params = []
            
            if text is not None:
                updates.append("text = %s")
                params.append(text.strip())
            if completed is not None:
                updates.append("completed = %s")
                params.append(completed)
            if color is not None:
                updates.append("color = %s")
                params.append(color)
            
            updates.append("updated_at = %s")
            params.append(self._get_current_timestamp())
            params.append(todo_id)

            cursor.execute(f"""
                UPDATE todos SET {', '.join(updates)}
                WHERE id = %s
            """, params)

            conn.commit()
            conn.close()

            return self.get_todo_by_id(todo_id, user_id)

        except Exception as e:
            return None

    def toggle_todo(self, todo_id: str, user_id: Optional[str] = None) -> Optional[Dict]:
        """Toggle todo completion status"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get current todo
            if user_id:
                cursor.execute("""
                    SELECT completed FROM todos WHERE id = %s AND user_id = %s
                """, (todo_id, user_id))
            else:
                cursor.execute("""
                    SELECT completed FROM todos WHERE id = %s AND user_id IS NULL
                """, (todo_id,))

            todo = cursor.fetchone()
            if not todo:
                conn.close()
                return None

            # Toggle completion
            new_completed = not todo[0]
            updated_at = self._get_current_timestamp()

            cursor.execute("""
                UPDATE todos SET completed = %s, updated_at = %s
                WHERE id = %s
            """, (new_completed, updated_at, todo_id))

            conn.commit()
            conn.close()

            return self.get_todo_by_id(todo_id, user_id)

        except Exception as e:
            return None

    def delete_todo(self, todo_id: str, user_id: Optional[str] = None) -> Optional[Dict]:
        """Delete a todo"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get todo before deletion
            if user_id:
                cursor.execute("""
                    SELECT id, user_id, text, color, completed, created_at, updated_at
                    FROM todos WHERE id = %s AND user_id = %s
                """, (todo_id, user_id))
            else:
                cursor.execute("""
                    SELECT id, user_id, text, color, completed, created_at, updated_at
                    FROM todos WHERE id = %s AND user_id IS NULL
                """, (todo_id,))

            todo = cursor.fetchone()
            if not todo:
                conn.close()
                return None

            # Delete todo
            cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            conn.commit()
            conn.close()

            return self._to_dict(todo)

        except Exception as e:
            return None

    def get_guest_todo_count(self) -> int:
        """Get count of guest todos"""
        return self.user_service.get_guest_todo_count()

    def get_completed_todos(self, user_id: Optional[str] = None) -> List[Dict]:
        """Get completed todos for a user or guest"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if user_id:
                cursor.execute("""
                    SELECT id, user_id, text, color, completed, created_at, updated_at
                    FROM todos WHERE user_id = %s AND completed = 1
                    ORDER BY created_at DESC
                """, (user_id,))
            else:
                cursor.execute("""
                    SELECT id, user_id, text, color, completed, created_at, updated_at
                    FROM todos WHERE user_id IS NULL AND completed = 1
                    ORDER BY created_at DESC
                """)

            todos = cursor.fetchall()
            conn.close()

            return [self._to_dict(todo) for todo in todos]

        except Exception as e:
            return []

    def delete_all_todos(self, user_id: Optional[str] = None) -> int:
        """Delete all todos for a user or guest"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if user_id:
                cursor.execute("DELETE FROM todos WHERE user_id = %s", (user_id,))
            else:
                cursor.execute("DELETE FROM todos WHERE user_id IS NULL")

            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()

            return deleted_count

        except Exception as e:
            return 0

    def get_todo_count(self, user_id: Optional[str] = None) -> int:
        """Get todo count for a user or guest"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if user_id:
                cursor.execute("SELECT COUNT(*) FROM todos WHERE user_id = %s", (user_id,))
            else:
                cursor.execute("SELECT COUNT(*) FROM todos WHERE user_id IS NULL")

            count = cursor.fetchone()[0]
            conn.close()

            return count

        except Exception as e:
            return 0

    def _to_dict(self, todo: tuple) -> Dict:
        """Convert database tuple to dictionary"""
        return {
            'id': todo[0],
            'user_id': todo[1],
            'text': todo[2],
            'color': todo[3],
            'completed': bool(todo[4]),
            'createdAt': todo[5],
            'updatedAt': todo[6]
        }

todo_service = TodoService()