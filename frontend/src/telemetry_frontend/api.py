from __future__ import annotations

import pandas as pd
import requests
import streamlit as st


def fetch_feedback_data(api_url: str) -> pd.DataFrame:
    """Fetch telemetry rows from the backend API."""
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to backend at {api_url}.")
    except requests.exceptions.Timeout:
        st.error(f"Timed out while connecting to backend at {api_url}.")
    except requests.exceptions.RequestException as exc:
        st.error(f"Backend request failed: {exc}")
    except ValueError as exc:
        st.error(f"Backend response was not valid JSON: {exc}")

    return pd.DataFrame()
