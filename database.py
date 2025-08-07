import os
import sqlite3
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./todo_app.db')
db_path = Path('./todo_app.db')
db_path.parent.mkdir(exist_ok=True)

def get_database():
    return sqlite3.connect('./todo_app.db', check_same_thread=False)

db = get_database() 