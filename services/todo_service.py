import uuid
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, Session
from database import SessionLocal, engine

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(String, primary_key=True, index=True)
    text = Column(String, nullable=False)
    color = Column(String, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

# Ensure table is created (for dev convenience)
Base.metadata.create_all(bind=engine)

class TodoService:
    def _init_(self):
        pass

    def get_all_todos(self) -> List[Dict]:
        with SessionLocal() as db:
            todos = db.query(Todo).order_by(Todo.created_at.desc()).all()
            print("[ALL TODOS IDS]", [t.id for t in todos])
            return [self._to_dict(todo) for todo in todos]

    def get_completed_todos(self) -> List[Dict]:
        with SessionLocal() as db:
            todos = db.query(Todo).filter(Todo.completed == True).order_by(Todo.created_at.desc()).all()
            return [self._to_dict(todo) for todo in todos]

    def get_todo_by_id(self, todo_id: str) -> Optional[Dict]:
        with SessionLocal() as db:
            all_ids = [t.id for t in db.query(Todo).all()]
            print("[GET BY ID] All IDs:", all_ids)
            print("Looking for todo_id:", repr(todo_id))
            todo = db.query(Todo).filter(Todo.id == todo_id.strip()).first()
            print("Found todo:", todo)
            return self._to_dict(todo) if todo else None

    def create_todo(self, text: str, color: Optional[str] = None) -> Dict:
        if not text or not text.strip():
            raise ValueError("Text is required")
        todo_id = str(uuid.uuid4())
        created_at = datetime.now()
        new_todo = Todo(
            id=todo_id,
            text=text.strip(),
            color=color,
            completed=False,
            created_at=created_at
        )
        with SessionLocal() as db:
            db.add(new_todo)
            db.commit()
            db.refresh(new_todo)
        return self._to_dict(new_todo)

    def update_todo(self, todo_id: str, text: Optional[str] = None, completed: Optional[bool] = None, color: Optional[str] = None) -> Optional[Dict]:
        with SessionLocal() as db:
            all_ids = [t.id for t in db.query(Todo).all()]
            print("[UPDATE] All IDs:", all_ids)
            print("[UPDATE] Looking for todo_id:", repr(todo_id))
            todo = db.query(Todo).filter(Todo.id == todo_id.strip()).first()
            print("[UPDATE] Found todo:", todo)
            if not todo:
                return None
            if text is not None:
                todo.text = text.strip()
            if completed is not None:
                todo.completed = completed
            if color is not None:
                todo.color = color
            todo.updated_at = datetime.now()
            db.commit()
            db.refresh(todo)
            return self._to_dict(todo)

    def toggle_todo(self, todo_id: str) -> Optional[Dict]:
        with SessionLocal() as db:
            all_ids = [t.id for t in db.query(Todo).all()]
            print("[TOGGLE] All IDs:", all_ids)
            print("[TOGGLE] Looking for todo_id:", repr(todo_id))
            todo = db.query(Todo).filter(Todo.id == todo_id.strip()).first()
            print("[TOGGLE] Found todo:", todo)
            if not todo:
                return None
            todo.completed = not todo.completed
            todo.updated_at = datetime.now()
            db.commit()
            db.refresh(todo)
            return self._to_dict(todo)

    def delete_todo(self, todo_id: str) -> Optional[Dict]:
        with SessionLocal() as db:
            all_ids = [t.id for t in db.query(Todo).all()]
            print("[DELETE] All IDs:", all_ids)
            print("[DELETE] Looking for todo_id:", repr(todo_id))
            todo = db.query(Todo).filter(Todo.id == todo_id.strip()).first()
            print("[DELETE] Found todo:", todo)
            if not todo:
                return None
            result = self._to_dict(todo)
            db.delete(todo)
            db.commit()
            return result

    def delete_all_todos(self) -> int:
        with SessionLocal() as db:
            count = db.query(Todo).count()
            db.query(Todo).delete()
            db.commit()
            return count

    def get_todo_count(self) -> int:
        with SessionLocal() as db:
            return db.query(Todo).count()

    def _to_dict(self, todo: Todo) -> Dict:
        return {
            'id': todo.id,
            'text': todo.text,
            'color': todo.color,
            'completed': todo.completed,
            'createdAt': todo.created_at.isoformat() if todo.created_at else None,
            'updatedAt': todo.updated_at.isoformat() if todo.updated_at else None
        }

todo_service = TodoService()