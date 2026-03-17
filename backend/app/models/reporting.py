from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class HomeResponse(BaseModel):
    message: str
    docs_url: str
    dashboard_hint: str


class ApiMessageResponse(BaseModel):
    status: str
    message: str


class TriggerCount(BaseModel):
    reason: str
    count: int = Field(..., ge=0)


class FeedbackRecordResponse(BaseModel):
    id: int
    student_id: str
    timestamp: datetime
    trigger_reason: str
    file_path: str | None = None
    line_range: str | None = None
    excerpt: str | None = None
    ai_reasoning_summary: str | None = None
    report_date: date | None = None


class DailyReportPreviewResponse(BaseModel):
    student_id: str
    report_count: int = Field(..., ge=0)
    latest_timestamp: datetime | None = None
    latest_summary: str | None = None
    latest_trigger_reason: str | None = None
    triggers: list[TriggerCount]
    attention_score: int = Field(..., ge=0, le=100)
    progress_score: int = Field(..., ge=0, le=100)
    needs_attention: bool


class DailyReportsPageResponse(BaseModel):
    items: list[DailyReportPreviewResponse]
    next_cursor: str | None = None
    total_count: int = Field(..., ge=0)


class StudentFollowUpResponse(BaseModel):
    student_id: str
    report_count: int = Field(..., ge=0)
    latest_summary: str
    attention_score: int = Field(..., ge=0, le=100)


class GroupSummaryResponse(BaseModel):
    report_date: date
    report_count: int = Field(..., ge=0)
    student_count: int = Field(..., ge=0)
    needs_attention_count: int = Field(..., ge=0)
    top_reasons: list[TriggerCount]
    key_concepts: list[str]
    students_needing_follow_up: list[StudentFollowUpResponse]
    recommended_actions: list[str]
    narrative: str


class StudentReportDetailResponse(DailyReportPreviewResponse):
    reports: list[FeedbackRecordResponse]
