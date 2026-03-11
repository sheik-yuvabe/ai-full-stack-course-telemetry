from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.models.feedback import FeedbackPayload
from app.services.feedback import create_feedback, list_feedback


router = APIRouter()


@router.post("/feedback")
async def submit_feedback(payload: FeedbackPayload) -> dict[str, str]:
    create_feedback(payload)
    return {"status": "ok", "message": "Data stored in SQLite"}


@router.get("/api/data")
async def get_data() -> list[dict[str, Any]]:
    return list_feedback()
