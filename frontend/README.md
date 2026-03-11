# Telemetry Frontend

This frontend is a Streamlit dashboard for viewing telemetry events produced by the backend API.

The repository-level `.gitignore` already ignores `.env`, `.venv`, `venv`, and other local-only files, so your frontend secrets and virtual environment stay out of git.

## Structure

```text
frontend/
  README.md
  requirements.txt
  src/
    app.py
    telemetry_frontend/
      api.py
      config.py
      dashboard.py
```

## Local setup

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run src/app.py
```

## Configuration

The app loads `frontend/.env` automatically. Set `BACKEND_API_URL` there if you want the dashboard to point to a local backend instead of the deployed Hugging Face endpoint.

```powershell
BACKEND_API_URL=http://127.0.0.1:8000/api/data
```
