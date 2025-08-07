import sqlite3
from pathlib import Path
from schema import TODOS_TABLE_SCHEMA

def create_tables():
    db_path = Path('./todo_app.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(TODOS_TABLE_SCHEMA)
    conn.commit()
    conn.close()
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables() 