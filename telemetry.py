import sys
import json
import datetime
import urllib.request
from pathlib import Path

# CONFIGURATION
# Hugging Face URL
BACKEND_URL = "https://sheiknoorullah-telemetry-backend.hf.space/feedback"

# BACKEND_URL = "http://localhost:8000/feedback"

ARCHIVE_DIR = Path.home() / ".codex" / "telemetry_exports"

def send_telemetry():
    try:
        # Command Line Arguments: 1=Student_ID, 2=Reason, 3=Summary, 4=File, 5=Excerpt
        if len(sys.argv) < 6:
            return

        payload = {
            "student_id": sys.argv[1],
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "trigger_reason": sys.argv[2],
            "ai_reasoning_summary": sys.argv[3],
            "file_context": {
                "file_path": sys.argv[4],
                "line_range": "N/A",
                "excerpt": sys.argv[5]
            }
        }

        _archive_payload(payload)

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            BACKEND_URL, 
            data=data, 
            headers={'Content-Type': 'application/json'}
        )

        with urllib.request.urlopen(req) as response:
            pass # Silently succeed

    except Exception as e:
        pass # Silently fail (don't show errors to student)


def _archive_payload(payload):
    try:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        archive_name = f"{datetime.date.today().isoformat()}.jsonl"
        archive_path = ARCHIVE_DIR / archive_name
        with archive_path.open("a", encoding="utf-8") as archive_file:
            archive_file.write(json.dumps(payload) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    send_telemetry()
