import subprocess
import sys
import time
from pathlib import Path


def test_app_stays_running_when_started_directly():
    app_path = Path(__file__).resolve().parents[1] / "src" / "app.py"
    proc = subprocess.Popen(
        [sys.executable, str(app_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        time.sleep(2)
        assert proc.poll() is None, "The app exited immediately instead of staying alive as a server."
    finally:
        if proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=10)
