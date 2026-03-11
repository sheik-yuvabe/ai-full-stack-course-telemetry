from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


PAGE_TITLE = "AI Mentor Dashboard"
PROJECT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_DIR / ".env")
BACKEND_API_URL = os.getenv("BACKEND_API_URL")
