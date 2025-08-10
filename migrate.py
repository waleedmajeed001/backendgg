import os
import sqlite3
import psycopg2
from database import get_db_connection, DATABASE_URL
from schema import TODOS_TABLE_SCHEMA, USERS_TABLE_SCHEMA

def create_tables():
    if DATABASE_URL.startswith('postgresql://'):
        # Use PostgreSQL for Neon
        print("🗄️ Using PostgreSQL database (Neon)")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Create tables in order (users first, then todos due to foreign key)
            cursor.execute(USERS_TABLE_SCHEMA)
            cursor.execute(TODOS_TABLE_SCHEMA)
            conn.commit()
            
            # Verify the tables were created correctly
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'todos' 
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            print("📋 Todos table columns:")
            for col in columns:
                print(f"  - {col[0]} ({col[1]})")
            
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users' 
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            print("📋 Users table columns:")
            for col in columns:
                print(f"  - {col[0]} ({col[1]})")
            
            conn.close()
            print("✅ PostgreSQL tables created successfully!")
            
        except Exception as e:
            print(f"❌ Error creating PostgreSQL tables: {e}")
            print("💡 Make sure your DATABASE_URL is correct in .env file")
            
    else:
        # Use SQLite for local development
        print("🗄️ Using SQLite database (local)")
        db_file = 'todo_app.db'
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"🗑️ Removed existing database: {db_file}")
        
        with sqlite3.connect(db_file) as conn:
            # Create tables in order (users first, then todos due to foreign key)
            conn.execute(USERS_TABLE_SCHEMA)
            conn.execute(TODOS_TABLE_SCHEMA)
            conn.commit()
            
            # Verify the tables were created correctly
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(todos)")
            columns = cursor.fetchall()
            print("📋 Todos table columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            print("📋 Users table columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        
        print("✅ SQLite tables created successfully!")

if __name__ == "__main__":
    create_tables()