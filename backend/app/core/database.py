from __future__ import annotations

import sqlite3

from app.core.config import DB_PATH


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                trigger_reason TEXT NOT NULL,
                file_path TEXT,
                line_range TEXT,
                excerpt TEXT,
                ai_reasoning_summary TEXT
            )
            """
        )
        connection.commit()
