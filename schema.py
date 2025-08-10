TODOS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS todos (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    color TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
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