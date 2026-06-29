"""Szkielet generowania 3D przez Doubao Seed3D 2.0 (Volcengine Ark).

⚠️ DRAFT — dokładny endpoint i kształt payloadu dla Seed3D należy potwierdzić w
dokumentacji Ark po uzyskaniu dostępu. Zakładamy wzorzec async:
    submit -> task_id -> polling statusu -> URL wyniku.

Użycie (po uzupełnieniu ../.env -> ARK_API_KEY):
    python seed3d/generate_3d.py "opis obiektu 3D"
"""
import os
import sys
import time

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
load_dotenv(ENV_PATH)

API_KEY = os.getenv("ARK_API_KEY")
BASE_URL = os.getenv("ARK_BASE_URL")
MODEL = os.getenv("SEED3D_MODEL", "doubao-seed3d-2-0")

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def submit(prompt: str) -> str:
    """Wysyła zadanie generacji 3D, zwraca task_id."""
    # TODO: potwierdzić ścieżkę endpointu Seed3D w dokumentacji Ark.
    url = f"{BASE_URL}/contents/generations/tasks"
    payload = {"model": MODEL, "content": [{"type": "text", "text": prompt}]}
    r = requests.post(url, headers=HEADERS, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data.get("id") or data.get("task_id")


def poll(task_id: str, interval: int = 5, timeout: int = 600) -> dict:
    """Odpytuje status zadania aż do zakończenia."""
    url = f"{BASE_URL}/contents/generations/tasks/{task_id}"
    waited = 0
    while waited < timeout:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
        status = data.get("status")
        print(f"  status: {status} ({waited}s)")
        if status in ("succeeded", "SUCCEEDED", "success"):
            return data
        if status in ("failed", "FAILED", "error"):
            raise RuntimeError(f"Zadanie nieudane: {data}")
        time.sleep(interval)
        waited += interval
    raise TimeoutError("Przekroczono czas oczekiwania na wynik.")


def main():
    if not API_KEY:
        sys.exit("❌ Brak ARK_API_KEY w .env (skopiuj .env.example -> .env).")
    prompt = sys.argv[1] if len(sys.argv) > 1 else "a small cute robot, low-poly"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"▶ Model: {MODEL}\n▶ Prompt: {prompt}")
    task_id = submit(prompt)
    print(f"▶ task_id: {task_id}")
    result = poll(task_id)
    print("✅ Gotowe. Wynik:")
    print(result)


if __name__ == "__main__":
    main()
