from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class FileContext(BaseModel):
    file_path: str = Field(..., min_length=1)
    line_range: str = Field(..., min_length=1)
    excerpt: str = Field(..., min_length=1)


class FeedbackPayload(BaseModel):
    student_id: str = Field(..., min_length=1)
    timestamp: datetime
    trigger_reason: Literal[
        "compiler_error",
        "conceptual_doubt",
        "repeated_failure",
        "understanding_gap",
        "session_summary",
        "tool_misuse",
        "other",
    ]
    file_context: FileContext
    ai_reasoning_summary: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")
