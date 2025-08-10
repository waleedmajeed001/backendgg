import sqlite3
import uuid
import hashlib
import datetime
from typing import Dict, Optional, Tuple
from database import get_db_connection
from schema import USERS_COLUMNS

class UserService:
    def __init__(self):
        self.db_path = 'todo_app.db'

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _generate_id(self) -> str:
        """Generate unique user ID"""
        return str(uuid.uuid4())

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.datetime.now().isoformat()

    def register_user(self, email: str, password: str, name: str) -> Tuple[bool, str, Optional[Dict]]:
        """Register a new user"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                conn.close()
                return False, "User with this email already exists", None

            # Create new user
            user_id = self._generate_id()
            hashed_password = self._hash_password(password)
            created_at = self._get_current_timestamp()

            cursor.execute("""
                INSERT INTO users (id, email, password, name, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, email, hashed_password, name, created_at, created_at))

            conn.commit()
            conn.close()

            # Return user data without password
            user_data = {
                'id': user_id,
                'email': email,
                'name': name,
                'created_at': created_at
            }

            return True, "User registered successfully", user_data

        except Exception as e:
            return False, f"Registration failed: {str(e)}", None

    def login_user(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Authenticate user login"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            hashed_password = self._hash_password(password)

            cursor.execute("""
                SELECT id, email, password, name, created_at, updated_at
                FROM users WHERE email = %s AND password = %s
            """, (email, hashed_password))

            user = cursor.fetchone()
            conn.close()

            if user:
                user_data = {
                    'id': user[0],
                    'email': user[1],
                    'name': user[3],
                    'created_at': user[4],
                    'updated_at': user[5]
                }
                return True, "Login successful", user_data
            else:
                return False, "Invalid email or password", None

        except Exception as e:
            return False, f"Login failed: {str(e)}", None

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, email, name, created_at, updated_at
                FROM users WHERE id = %s
            """, (user_id,))

            user = cursor.fetchone()
            conn.close()

            if user:
                return {
                    'id': user[0],
                    'email': user[1],
                    'name': user[2],
                    'created_at': user[3],
                    'updated_at': user[4]
                }
            return None

        except Exception as e:
            return None

    def get_guest_todo_count(self) -> int:
        """Get count of todos without user_id (guest todos)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM todos WHERE user_id IS NULL")
            count = cursor.fetchone()[0]
            conn.close()

            return count

        except Exception as e:
            return 0
