USERS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
"""

TODOS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS todos (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    text TEXT NOT NULL,
    color VARCHAR(50),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

USERS_COLUMNS = [
    'id',
    'email',
    'password',
    'name',
    'created_at',
    'updated_at'
]

TODOS_COLUMNS = [
    'id',
    'user_id',
    'text', 
    'color',
    'completed',
    'created_at',
    'updated_at'
]