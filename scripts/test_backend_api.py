import subprocess
import sys
import time
import urllib.request
import json


def main():
    # Start uvicorn
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        cwd="backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(4)

    base = "http://127.0.0.1:8000"
    results = []

    # Test login
    req = urllib.request.Request(
        f"{base}/api/v1/auth/login",
        data=json.dumps(
            {"email": "demo@salespredict.ai", "password": "demo123"}
        ).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            login_data = json.loads(resp.read())
            token = login_data.get("access_token", "")
            results.append(f"Login: OK (token length {len(token)})")
    except Exception as e:
        results.append(f"Login: FAIL - {e}")
        token = ""

    # Test sales list
    try:
        with urllib.request.urlopen(f"{base}/api/v1/sales?limit=3") as resp:
            sales = json.loads(resp.read())
            results.append(f"Sales list: OK ({len(sales)} items)")
    except Exception as e:
        results.append(f"Sales list: FAIL - {e}")

    # Test aggregates
    try:
        url = f"{base}/api/v1/sales/aggregates/daterange?start_date=2025-01-01&end_date=2026-12-31&group_by=month"
        with urllib.request.urlopen(url) as resp:
            agg = json.loads(resp.read())
            results.append(f"Aggregates: OK ({len(agg)} periods)")
    except Exception as e:
        results.append(f"Aggregates: FAIL - {e}")

    # Kill uvicorn
    proc.terminate()
    proc.wait(timeout=5)

    for r in results:
        print(r)


if __name__ == "__main__":
    main()
