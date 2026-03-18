from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, datetime
import re
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
        return [_serialize_feedback_row(dict(row)) for row in rows]


def list_feedback_by_date(report_date: date) -> list[dict[str, Any]]:
    return [
        row
        for row in list_feedback()
        if row.get("report_date") == report_date.isoformat()
    ]


def list_report_dates() -> list[str]:
    dates = {
        row["report_date"]
        for row in list_feedback()
        if row.get("report_date")
    }
    return sorted(dates, reverse=True)


def list_daily_reports(
    report_date: date,
    *,
    limit: int = 8,
    cursor: str | None = None,
    search: str | None = None,
    attention_only: bool = False,
) -> dict[str, Any]:
    reports = _build_student_reports(report_date)
    reports = _filter_reports(reports, search=search, attention_only=attention_only)

    start_index = _decode_cursor(cursor)
    end_index = start_index + limit
    paged_reports = reports[start_index:end_index]

    return {
        "items": [_to_report_preview(report) for report in paged_reports],
        "next_cursor": str(end_index) if end_index < len(reports) else None,
        "total_count": len(reports),
    }


def get_student_report_detail(report_date: date, student_id: str) -> dict[str, Any] | None:
    reports = _build_student_reports(report_date)
    for report in reports:
        if report["student_id"] == student_id:
            return report
    return None


def summarize_daily_reports(report_date: date) -> dict[str, Any]:
    feedback_rows = list_feedback_by_date(report_date)
    if not feedback_rows:
        return {
            "report_date": report_date.isoformat(),
            "report_count": 0,
            "student_count": 0,
            "needs_attention_count": 0,
            "top_reasons": [],
            "key_concepts": [],
            "students_needing_follow_up": [],
            "recommended_actions": [],
            "narrative": "No reports were recorded for this day.",
        }

    daily_reports = _build_student_reports(report_date)
    reason_counts = Counter(row.get("trigger_reason") or "other" for row in feedback_rows)
    top_reasons = [
        {"reason": reason, "count": count}
        for reason, count in reason_counts.most_common(5)
    ]
    key_concepts = _extract_key_concepts(feedback_rows)
    follow_up_students = [
        {
            "student_id": report["student_id"],
            "report_count": report["report_count"],
            "latest_summary": report.get("latest_summary") or "No summary provided.",
            "attention_score": report["attention_score"],
        }
        for report in daily_reports[:5]
        if report["needs_attention"]
    ]

    return {
        "report_date": report_date.isoformat(),
        "report_count": len(feedback_rows),
        "student_count": len(daily_reports),
        "needs_attention_count": sum(1 for report in daily_reports if report["needs_attention"]),
        "top_reasons": top_reasons,
        "key_concepts": key_concepts,
        "students_needing_follow_up": follow_up_students,
        "recommended_actions": _build_recommended_actions(top_reasons),
        "narrative": _build_group_narrative(
            report_date=report_date,
            report_count=len(feedback_rows),
            student_count=len(daily_reports),
            top_reasons=top_reasons,
            key_concepts=key_concepts,
        ),
    }


def _build_student_reports(report_date: date) -> list[dict[str, Any]]:
    feedback_rows = list_feedback_by_date(report_date)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in feedback_rows:
        grouped[row.get("student_id") or "Unknown"].append(row)

    reports: list[dict[str, Any]] = []
    for student_id, items in grouped.items():
        sorted_items = sorted(
            items,
            key=lambda item: item.get("timestamp", ""),
            reverse=True,
        )
        trigger_counts = Counter(item.get("trigger_reason") or "other" for item in sorted_items)
        latest_report = sorted_items[0]
        attention_score = _calculate_attention_score(
            triggers=trigger_counts,
            report_count=len(sorted_items),
        )
        reports.append(
            {
                "student_id": student_id,
                "report_count": len(sorted_items),
                "latest_timestamp": latest_report.get("timestamp"),
                "latest_summary": latest_report.get("ai_reasoning_summary"),
                "latest_trigger_reason": latest_report.get("trigger_reason"),
                "triggers": [
                    {"reason": reason, "count": count}
                    for reason, count in trigger_counts.most_common()
                ],
                "attention_score": attention_score,
                "progress_score": max(5, 100 - attention_score),
                "needs_attention": attention_score >= 55,
                "reports": sorted_items,
            }
        )

    return sorted(
        reports,
        key=lambda item: (
            item["needs_attention"],
            item["attention_score"],
            item["report_count"],
            item.get("latest_timestamp") or "",
        ),
        reverse=True,
    )


def _filter_reports(
    reports: list[dict[str, Any]],
    *,
    search: str | None,
    attention_only: bool,
) -> list[dict[str, Any]]:
    filtered = reports

    if search:
        lowered = search.strip().lower()
        filtered = [
            report
            for report in filtered
            if lowered in report["student_id"].lower()
        ]

    if attention_only:
        filtered = [report for report in filtered if report["needs_attention"]]

    return filtered


def _to_report_preview(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "student_id": report["student_id"],
        "report_count": report["report_count"],
        "latest_timestamp": report["latest_timestamp"],
        "latest_summary": report["latest_summary"],
        "latest_trigger_reason": report["latest_trigger_reason"],
        "triggers": report["triggers"],
        "attention_score": report["attention_score"],
        "progress_score": report["progress_score"],
        "needs_attention": report["needs_attention"],
    }


def _calculate_attention_score(
    *,
    triggers: Counter[str],
    report_count: int,
) -> int:
    score = 18
    score += min(report_count * 9, 24)
    score += triggers.get("repeated_failure", 0) * 18
    score += triggers.get("understanding_gap", 0) * 16
    score += triggers.get("conceptual_doubt", 0) * 12
    score += triggers.get("compiler_error", 0) * 7
    score += triggers.get("session_summary", 0) * 3
    return min(score, 100)


def _decode_cursor(cursor: str | None) -> int:
    if not cursor:
        return 0

    try:
        return max(int(cursor), 0)
    except ValueError:
        return 0


def _serialize_feedback_row(row: dict[str, Any]) -> dict[str, Any]:
    report_date = _extract_report_date(row.get("timestamp"))
    if report_date:
        row["report_date"] = report_date.isoformat()
    else:
        row["report_date"] = None
    return row


def _extract_report_date(timestamp_value: Any) -> date | None:
    if not timestamp_value:
        return None

    timestamp_str = str(timestamp_value)
    normalized = timestamp_str.replace("Z", "+00:00")

    try:
        return datetime.fromisoformat(normalized).date()
    except ValueError:
        return None


def _extract_key_concepts(rows: list[dict[str, Any]]) -> list[str]:
    structured_gap_counts: Counter[str] = Counter()
    structured_lesson_counts: Counter[str] = Counter()
    structured_labels: dict[str, str] = {}

    for row in rows:
        summary = row.get("ai_reasoning_summary") or ""

        gap_value = _extract_structured_field(summary, "Gap")
        if gap_value:
            normalized_gap = _normalize_phrase(gap_value)
            structured_gap_counts[normalized_gap] += 1
            structured_labels.setdefault(normalized_gap, gap_value.strip())

        lesson_value = _extract_structured_field(summary, "Lesson")
        if lesson_value:
            normalized_lesson = _normalize_phrase(lesson_value)
            structured_lesson_counts[normalized_lesson] += 1
            structured_labels.setdefault(normalized_lesson, lesson_value.strip())

    if structured_gap_counts:
        return [
            structured_labels[key]
            for key, _count in structured_gap_counts.most_common(5)
        ]

    if structured_lesson_counts:
        return [
            structured_labels[key]
            for key, _count in structured_lesson_counts.most_common(5)
        ]

    token_counts: Counter[str] = Counter()
    stop_words = {
        "the",
        "and",
        "with",
        "from",
        "that",
        "this",
        "they",
        "their",
        "into",
        "have",
        "been",
        "were",
        "task",
        "lesson",
        "student",
        "course",
        "current",
        "needs",
        "need",
        "more",
        "about",
        "during",
        "after",
        "before",
        "while",
        "showed",
        "shows",
        "could",
        "would",
        "should",
        "report",
        "reports",
        "summary",
        "understanding",
    }

    for row in rows:
        summary = (row.get("ai_reasoning_summary") or "").lower()
        words = re.findall(r"[a-z][a-z_]{3,}", summary)
        for word in words:
            if word not in stop_words:
                token_counts[word.replace("_", " ")] += 1

    return [word for word, _count in token_counts.most_common(5)]


def _extract_structured_field(summary: str, field_name: str) -> str | None:
    pattern = re.compile(
        rf"{re.escape(field_name)}:\s*(.+?)(?=(?:Lesson|Task|Assessment|Gap|Tutor action):|$)",
        flags=re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(summary)
    if not match:
        return None
    return match.group(1).strip().rstrip(".")


def _normalize_phrase(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _build_recommended_actions(top_reasons: list[dict[str, Any]]) -> list[str]:
    actions: list[str] = []
    reason_map = {
        "compiler_error": "Add a short debugging clinic with trace-reading and syntax triage examples.",
        "conceptual_doubt": "Revisit the theory explanation with one worked example before assigning more practice.",
        "repeated_failure": "Schedule guided practice and reduce task complexity until the student can complete one attempt independently.",
        "understanding_gap": "Check whether the student can explain the lesson concept in plain language before continuing to the next task.",
        "session_summary": "Use the session summary to personalize the next activity rather than reacting to each isolated error.",
    }

    for item in top_reasons:
        action = reason_map.get(item["reason"])
        if action and action not in actions:
            actions.append(action)

    if not actions:
        actions.append("Review the individual reports and identify the next lesson checkpoint that should be retaught.")

    return actions


def _build_group_narrative(
    *,
    report_date: date,
    report_count: int,
    student_count: int,
    top_reasons: list[dict[str, Any]],
    key_concepts: list[str],
) -> str:
    if top_reasons:
        reason_text = ", ".join(
            f"{item['reason']} ({item['count']})" for item in top_reasons[:3]
        )
    else:
        reason_text = "no dominant blocker patterns"

    return (
        f"On {report_date.isoformat()}, {student_count} students generated {report_count} tutor-facing reports. "
        f"The strongest blocker patterns were {reason_text}. "
        "Use the blocker list below to decide what should be retaught first."
    )
