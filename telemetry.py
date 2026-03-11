import sys
import json
import datetime
import urllib.request

# CONFIGURATION
# Hugging Face URL
BACKEND_URL = "https://sheiknoorullah-telemetry-backend.hf.space/feedback"

# BACKEND_URL = "http://localhost:8000/feedback"

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

if __name__ == "__main__":
    send_telemetry()