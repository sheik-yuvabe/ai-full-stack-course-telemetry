from __future__ import annotations

from typing import Any

from app.core.database import get_connection
from app.models.feedback import FeedbackPayload


def create_feedback(payload: FeedbackPayload) -> None:
    timestamp_str = payload.timestamp.isoformat()

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO feedback (
                student_id,
                timestamp,
                trigger_reason,
                file_path,
                line_range,
                excerpt,
                ai_reasoning_summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.student_id,
                timestamp_str,
                payload.trigger_reason,
                payload.file_context.file_path,
                payload.file_context.line_range,
                payload.file_context.excerpt,
                payload.ai_reasoning_summary,
            ),
        )
        connection.commit()


def list_feedback() -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM feedback ORDER BY id DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
