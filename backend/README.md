# Telemetry Backend

This backend is a FastAPI service that accepts telemetry feedback and exposes stored events to the frontend dashboard.

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

The app loads `backend/.env` automatically. Update it if you want SQLite stored somewhere else or if you want to restrict CORS.

```powershell
TELEMETRY_DB_PATH=F:\path\to\telemetry.db
CORS_ALLOW_ORIGINS=http://localhost:8501
uvicorn app.main:app --reload
```
