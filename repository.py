from config import KEEP_MESSAGES
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

    return [
        {
            "role": row[0],
            "content": row[1]
        }
        for row in rows
    ]


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

def delete_old_messages(conversation_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM message
        WHERE conversation_id = ? AND id NOT IN (
            SELECT id FROM message
            WHERE conversation_id = ?
            ORDER BY id DESC
            LIMIT ?
        )
        """,
        (conversation_id, conversation_id, KEEP_MESSAGES),
    )

    conn.commit()
    conn.close()

def delete_conversation(conversation_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM message
        WHERE conversation_id = ?
        """,
        (conversation_id,),
    )

    cursor.execute(
        """
        DELETE FROM conversation
        WHERE id = ?
        """,
        (conversation_id,),
    )

    conn.commit()
    conn.close()