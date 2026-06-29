"""Generowanie wideo text→video przez DashScope (happyhorse-1.1-t2v).

Wzorzec async (zgodny z curl z dokumentacji):
    submit (X-DashScope-Async: enable) -> task_id -> polling -> URL wideo.

Użycie:
    python video/generate_video.py "opis sceny"
"""
import os
import sys
import time

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(ENV_PATH)

API_KEY = os.getenv("ALIBABA_API_KEY")
DS_URL = os.getenv("DASHSCOPE_BASE_URL")
MODEL = os.getenv("ALIBABA_VIDEO_MODEL", "happyhorse-1.1-t2v")

if not API_KEY or not DS_URL:
    sys.exit("❌ Brak ALIBABA_API_KEY / DASHSCOPE_BASE_URL w .env")

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def submit(prompt: str) -> str:
    url = f"{DS_URL}/services/aigc/video-generation/video-synthesis"
    r = requests.post(
        url,
        headers={**HEADERS, "X-DashScope-Async": "enable"},
        json={
            "model": MODEL,
            "input": {"prompt": prompt},
            "parameters": {"resolution": "720P", "ratio": "16:9", "duration": 5},
        },
        timeout=60,
    )
    print(f"submit -> {r.status_code}")
    r.raise_for_status()
    return r.json()["output"]["task_id"]


def poll(task_id: str, interval: int = 10, timeout: int = 900) -> dict:
    url = f"{DS_URL}/tasks/{task_id}"
    waited = 0
    while waited < timeout:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        out = r.json().get("output", {})
        status = out.get("task_status")
        print(f"  status: {status} ({waited}s)")
        if status == "SUCCEEDED":
            return out
        if status in ("FAILED", "CANCELED", "UNKNOWN"):
            raise RuntimeError(f"Zadanie nieudane: {out}")
        time.sleep(interval)
        waited += interval
    raise TimeoutError("Przekroczono czas oczekiwania.")


def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else (
        "A miniature city built from cardboard and bottle caps comes alive at night."
    )
    print(f"▶ Model: {MODEL}\n▶ Prompt: {prompt}")
    task_id = submit(prompt)
    print(f"▶ task_id: {task_id}")
    out = poll(task_id)
    print("✅ Gotowe. URL wideo:", out.get("video_url"))


if __name__ == "__main__":
    main()
