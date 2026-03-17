# Telemetry Frontend

This frontend is a React + Vite dashboard for reviewing daily telemetry reports produced by the backend API.

The repository-level `.gitignore` already ignores `.env`, virtual environments, `node_modules`, and build output, so local frontend configuration stays out of git.

## Structure

```text
frontend/
  README.md
  package.json
  index.html
  vite.config.js
  src/
    main.jsx
    App.jsx
    styles.css
```

## Local setup

```powershell
Copy-Item .env.example .env
npm install
npm run dev
```

Vite serves the app at `http://127.0.0.1:5173` by default.

## Configuration

Set `VITE_BACKEND_API_URL` in `frontend/.env` if you want the dashboard to point to a local backend instead of the deployed Hugging Face endpoint.

```powershell
VITE_BACKEND_API_URL=http://127.0.0.1:8000/api/data
```

The app derives the daily review endpoints from that base data URL:

- `/api/report-dates`
- `/api/daily-reports?report_date=YYYY-MM-DD&cursor=...&limit=8`
- `/api/student-report-detail?report_date=YYYY-MM-DD&student_id=...`
- `/api/group-summary?report_date=YYYY-MM-DD`

The UI defaults to the current date, uses a proper date picker, loads student cards with infinite scroll, and opens full report details in a drawer on demand.

## Production build

```powershell
npm run build
```
