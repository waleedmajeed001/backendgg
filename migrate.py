from sqlalchemy import text
from database import engine
from schema import TODOS_TABLE_SCHEMA

def create_tables():
    with engine.connect() as conn:
        # Drop the table if it exists to fix schema issues
        conn.execute(text("DROP TABLE IF EXISTS todos;"))
        conn.execute(text(TODOS_TABLE_SCHEMA))
        conn.commit()
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()