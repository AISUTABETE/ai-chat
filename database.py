import sqlite3


DB_PATH = "chat.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


def init_database():
    print("Initializing database...")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation(
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS message(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,

        FOREIGN KEY(conversation_id)
        REFERENCES conversation(id)
    )
    """)

    conn.commit()
    conn.close()
    
    print("Database initialized.")