import sqlite3
from database import get_connection


def insert_conversation(conversation_id: str, created_at: str):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversation(id, created_at)
        VALUES (?, ?)
        """,
        (conversation_id, created_at),
    )

    conn.commit()
    conn.close()


def insert_message(conversation_id: str, role: str, content: str, created_at: str):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO message(
            conversation_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (conversation_id, role, content, created_at),
    )

    conn.commit()
    conn.close()


def select_messages(conversation_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM message
        WHERE conversation_id=?
        ORDER BY id
        """,
        (conversation_id,),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# repository.py


def conversation_exists(conversation_id: str) -> bool:
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM conversation
        WHERE id = ?
        """,
        (conversation_id,),
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def count_messages(conversation_id: str) -> int:

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM message
        WHERE conversation_id=?
        """,
        (conversation_id,),
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count
