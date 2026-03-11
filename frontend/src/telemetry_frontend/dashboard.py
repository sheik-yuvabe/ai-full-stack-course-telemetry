from __future__ import annotations

import pandas as pd
import streamlit as st


DISPLAY_COLUMNS = [
    "timestamp",
    "student_id",
    "trigger_reason",
    "ai_reasoning_summary",
]


def render_dashboard(dataframe: pd.DataFrame, api_url: str) -> None:
    if dataframe.empty:
        st.warning("No telemetry data received yet.")
        st.caption(f"Connected to: {api_url}")
        return

    prepared_frame = _prepare_dataframe(dataframe)

    _render_metrics(prepared_frame)
    _render_table(prepared_frame)
    _render_student_detail(prepared_frame)

    st.caption(f"Connected to: {api_url}")


def _prepare_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    prepared_frame = dataframe.copy()

    if "timestamp" in prepared_frame.columns:
        prepared_frame["timestamp"] = pd.to_datetime(
            prepared_frame["timestamp"],
            format="mixed",
            utc=True,
            errors="coerce",
        )
        prepared_frame = prepared_frame.sort_values(
            by="timestamp",
            ascending=False,
            na_position="last",
        )

    return prepared_frame


def _render_metrics(dataframe: pd.DataFrame) -> None:
    total_col, students_col, blocker_col = st.columns(3)

    total_col.metric("Total Interventions", len(dataframe))

    if "student_id" in dataframe.columns:
        students_col.metric("Active Students", dataframe["student_id"].nunique())
    else:
        students_col.metric("Active Students", "N/A")

    if "trigger_reason" in dataframe.columns:
        modes = dataframe["trigger_reason"].mode()
        top_reason = modes.iloc[0] if not modes.empty else "N/A"
        blocker_col.metric("Top Blocker Pattern", top_reason)
    else:
        blocker_col.metric("Top Blocker Pattern", "N/A")


def _render_table(dataframe: pd.DataFrame) -> None:
    st.subheader("Current Pulse")
    available_columns = [column for column in DISPLAY_COLUMNS if column in dataframe.columns]

    st.dataframe(
        dataframe[available_columns],
        use_container_width=True,
        hide_index=True,
    )


def _render_student_detail(dataframe: pd.DataFrame) -> None:
    if "student_id" not in dataframe.columns:
        return

    st.subheader("Code Context Analysis")
    student_list = dataframe["student_id"].dropna().unique()
    selected_student = st.selectbox("Select student to inspect:", student_list)

    if not selected_student:
        return

    student_data = dataframe[dataframe["student_id"] == selected_student].iloc[0]
    details_col, code_col = st.columns([1, 2])

    with details_col:
        st.error(f"Reason: {student_data.get('trigger_reason', 'Unknown')}")
        st.info(f"AI logic: {student_data.get('ai_reasoning_summary', 'N/A')}")
        st.caption(f"Time: {student_data.get('timestamp')}")

    with code_col:
        file_path = student_data.get("file_path", "Unknown")
        line_range = student_data.get("line_range", "N/A")
        excerpt = student_data.get("excerpt", "# No code snippet provided")

        st.markdown(f"**File:** `{file_path}` | **Lines:** `{line_range}`")
        st.code(excerpt, language="python")
