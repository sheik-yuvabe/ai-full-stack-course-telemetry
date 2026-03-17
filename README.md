# AI Full-Stack Course Telemetry

This repository contains a small telemetry system for AI-assisted coding education:

- A FastAPI backend that receives tutor-facing telemetry reports and stores them in SQLite
- A React + Vite frontend designed for daily mentor review
- A Codex helper script and instruction file used to send curriculum-grounded learning reports

## Main use cases

- Summarize a student's understanding of the current lesson instead of logging every isolated error
- Send a compact tutor report with student ID, reason, summary, file path, and code excerpt
- Review daily student reports by date, then read a grouped cohort summary before drilling into individuals
- Save sent telemetry locally for later sharing and prompt refinement

## Repository structure

```text
ai-full-stack-course-telemetry/
  README.md
  AGENTS.md
  telemetry.py
  frontend/
  backend/
```

## Codex setup

This workflow assumes you are using Codex in your local environment and want telemetry to be sent automatically when students need help and the agent has enough evidence to produce a useful learning report.

### Codex access

As of March 11, 2026, OpenAI documents Codex as included with ChatGPT Plus, Pro, Business, and Enterprise/Edu plans. OpenAI also notes limited-time availability for some lower-tier plans, so plan details can change.

Official references:
- https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- https://openai.com/codex

### Where to place the two files

There are two important root-level files in this repository:

1. `AGENTS.md`
   Place this file at:
   `$HOME/.codex/AGENTS.md`

2. `telemetry.py`
   Place this file at:
   `$HOME/.codex/telemetry.py`

With both files in `$HOME/.codex/`, Codex can use the instruction file and the helper script together during student support sessions.

Copy them like this:

```powershell
New-Item -ItemType Directory -Force "$HOME/.codex"
Copy-Item .\AGENTS.md "$HOME/.codex/AGENTS.md"
Copy-Item .\telemetry.py "$HOME/.codex/telemetry.py"
```

### Update the backend URL in `telemetry.py`

Before using the telemetry workflow, open `$HOME/.codex/telemetry.py` and update the `BACKEND_URL` value so it points to your deployed backend.

Examples:

```python
BACKEND_URL = "https://your-backend-domain/feedback"
```

For local backend testing:

```python
BACKEND_URL = "http://127.0.0.1:8000/feedback"
```

### How the telemetry flow works

1. A student asks for help in Codex.
2. Codex follows the instructions in `$HOME/.codex/AGENTS.md`.
3. When there is enough evidence for a meaningful tutor note, Codex runs `$HOME/.codex/telemetry.py`.
4. `telemetry.py` sends the telemetry payload to your backend `/feedback` endpoint and also archives it locally in `$HOME/.codex/telemetry_exports/`.
5. The backend stores the report and the frontend dashboard displays both daily individual reports and a grouped summary.

## Clone the project

```powershell
git clone <your-repository-url>
cd ai-full-stack-course-telemetry
```

## Run the project

Open two terminals and start the backend first.

### 1. Run the backend

```powershell
cd backend
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Detailed backend instructions:
[backend/README.md](backend/README.md)

### 2. Run the frontend

In a second terminal:

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Detailed frontend instructions:
[frontend/README.md](frontend/README.md)

## Local development flow

- Start the backend on `http://127.0.0.1:8000`
- Point the frontend `VITE_BACKEND_API_URL` in `frontend/.env` to `http://127.0.0.1:8000/api/data`
- Open the Vite app at `http://127.0.0.1:5173`
- Send telemetry reports through `telemetry.py` or the backend API
- Review the daily summary first, then expand the student reports for that date

## Notes

- `.env` files, virtual environments, and the SQLite database are already ignored by git
- `frontend/.env` controls the backend API URL used by the dashboard
- `backend/.env` controls the SQLite path and CORS settings used by the API
- `$HOME/.codex/telemetry_exports/` stores a local JSONL archive of submitted telemetry sessions
