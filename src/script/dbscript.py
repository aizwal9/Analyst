import os
import psycopg2
from dotenv import load_dotenv

from src.db_config import get_db_connection

load_dotenv()


def init_history_db():
    """
    Creates the necessary tables for storing chat history
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print("Creating history tables...")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_sessions (
                thread_id TEXT PRIMARY KEY,
                title TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_messages(
                id SERIAL PRIMARY KEY,
                thread_id TEXT REFERENCES app_sessions(thread_id),
                role TEXT NOT NULL, -- 'user' or 'assistant'
                content TEXT,
                metadata JSONB, -- Stores SQL, Chart Config, Email Draft
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        print("Tables created successfully.")

    except Exception as e:
        print(f"Error creating tables : {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_history_db()