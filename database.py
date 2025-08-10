import os
import sqlite3
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///todo_app.db')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_connection():
    """Get a database connection (PostgreSQL for Neon, SQLite for local)"""
    if DATABASE_URL.startswith('postgresql://'):
        # Use PostgreSQL for Neon
        return psycopg2.connect(DATABASE_URL)
    else:
        # Use SQLite for local development
        return sqlite3.connect('todo_app.db')