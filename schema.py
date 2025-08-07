TODOS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS todos (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    color TEXT,
    completed INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT
);
"""

TODOS_COLUMNS = [
    'id',
    'text', 
    'color',
    'completed',
    'created_at',
    'updated_at'
] 