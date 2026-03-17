# Telemetry Backend

This backend is a FastAPI service that accepts telemetry feedback and exposes both raw events and daily teaching-review summaries to the frontend dashboard.

The repository-level `.gitignore` already ignores `.env`, `.venv`, `venv`, the SQLite database file, and other local-only files, so backend config and runtime data stay out of git.

## Structure

```text
backend/
  README.md
  requirements.txt
  telemetry.db
  main.py
  app/
    main.py
    api/
      routes.py
    core/
      config.py
      database.py
    models/
      feedback.py
    services/
      feedback.py
```

## Local setup

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The root `main.py` is kept as a compatibility shim, so `uvicorn main:app --reload` also works.

## Configuration

The app loads `backend/.env` automatically. Update it if you want SQLite stored somewhere else or if you want to restrict CORS for the React frontend.

```powershell
TELEMETRY_DB_PATH=F:\path\to\telemetry.db
CORS_ALLOW_ORIGINS=http://localhost:5173
uvicorn app.main:app --reload
```

## Review endpoints

The backend keeps the raw event feed and also exposes daily review helpers:

- `GET /api/data`
- `GET /api/data?report_date=YYYY-MM-DD`
- `GET /api/report-dates`
- `GET /api/daily-reports?report_date=YYYY-MM-DD&cursor=...&limit=8`
- `GET /api/student-report-detail?report_date=YYYY-MM-DD&student_id=...`
- `GET /api/group-summary?report_date=YYYY-MM-DD`
