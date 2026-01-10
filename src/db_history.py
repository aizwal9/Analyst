import json
from dotenv import load_dotenv

from src.db_config import get_db_connection

load_dotenv()

def ensure_session(thread_id : str, title : str = "New Analysis"):
    """
    Ensures a session exists. If not, creates one.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO app_sessions (thread_id, title) VALUES (%s, %s) ON CONFLICT (thread_id) DO NOTHING", (thread_id, title))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def save_message(thread_id : str, role : str, content : str, metadata : dict = None):
    """
    Saves a chat message to the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        meta_json = json.dumps(metadata) if metadata else None

        cursor.execute(
            "INSERT INTO app_messages (thread_id, role, content, metadata) VALUES (%s, %s, %s, %s)",
            (thread_id, role, content, meta_json)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_all_sessions():
    """
    Returns a list of all cht sessions
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT thread_id, title, created_at FROM app_sessions ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [{"thread_id": row[0], "title": row[1], "created_at": row[2]} for row in rows ]
    finally:
        cursor.close()
        conn.close()

def get_session_history(thread_id: str):
    """
    Returns full message history for a specific thread, including metadata.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT role,content,metadata FROM app_messages WHERE thread_id = %s ORDER BY created_at ASC", (thread_id,))

        messages = []
        for row in cursor.fetchall():
            role , content, metadata = row

            msg = {
                "role" : role,
                "content" : content
            }

            if metadata:
                meta = metadata if isinstance(metadata, dict) else json.loads(metadata)
                msg.update(meta)

            messages.append(msg)

        return messages
    finally:
        cursor.close()
        conn.close()