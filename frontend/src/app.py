import streamlit as st

from telemetry_frontend.api import fetch_feedback_data
from telemetry_frontend.config import BACKEND_API_URL, PAGE_TITLE
from telemetry_frontend.dashboard import render_dashboard


st.set_page_config(page_title=PAGE_TITLE, layout="wide")

st.title("Telemetry and Curriculum Engine")
st.caption("Real-time view of student struggles and AI interventions.")

if st.button("Refresh data"):
    st.rerun()

feedback_frame = fetch_feedback_data(BACKEND_API_URL)
render_dashboard(feedback_frame, BACKEND_API_URL)
