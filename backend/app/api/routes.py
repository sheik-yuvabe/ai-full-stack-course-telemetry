from __future__ import annotations

from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.models.feedback import FeedbackPayload
from app.models.reporting import (
    ApiMessageResponse,
    DailyReportsPageResponse,
    FeedbackRecordResponse,
    GroupSummaryResponse,
    HomeResponse,
    StudentReportDetailResponse,
)
from app.services.feedback import (
    create_feedback,
    get_student_report_detail,
    list_daily_reports,
    list_feedback,
    list_feedback_by_date,
    list_report_dates,
    summarize_daily_reports,
)


router = APIRouter()


@router.get("/", response_model=HomeResponse)
async def home() -> HomeResponse:
    return HomeResponse(
        message="Telemetry and Curriculum Engine API is running.",
        docs_url="/docs",
        dashboard_hint="Use the mentor dashboard frontend to review daily reports and group summaries.",
    )


@router.post("/feedback", response_model=ApiMessageResponse)
async def submit_feedback(payload: FeedbackPayload) -> ApiMessageResponse:
    create_feedback(payload)
    return ApiMessageResponse(status="ok", message="Data stored in SQLite")


@router.get("/api/data", response_model=list[FeedbackRecordResponse])
async def get_data(report_date: date | None = None) -> list[dict[str, Any]]:
    if report_date is None:
        return list_feedback()
    return list_feedback_by_date(report_date)


@router.get("/api/report-dates", response_model=list[date])
async def get_report_dates() -> list[str]:
    return list_report_dates()


@router.get("/api/daily-reports", response_model=DailyReportsPageResponse)
async def get_daily_reports(
    report_date: date,
    cursor: str | None = None,
    limit: int = Query(default=8, ge=1, le=24),
    search: str | None = None,
    attention_only: bool = False,
) -> dict[str, Any]:
    return list_daily_reports(
        report_date,
        cursor=cursor,
        limit=limit,
        search=search,
        attention_only=attention_only,
    )


@router.get("/api/student-report-detail", response_model=StudentReportDetailResponse)
async def get_student_detail(
    report_date: date,
    student_id: str,
) -> dict[str, Any]:
    detail = get_student_report_detail(report_date, student_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Student report not found")
    return detail


@router.get("/api/group-summary", response_model=GroupSummaryResponse)
async def get_group_summary(report_date: date) -> dict[str, Any]:
    return summarize_daily_reports(report_date)
