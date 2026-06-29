"""Czat z modelem Qwen (tryb OpenAI-compatible).

Użycie:
    python text/chat.py "Twoje pytanie"     # domyślny model: qwen-flash
"""
import os
import sys

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(ENV_PATH)

API_KEY = os.getenv("ALIBABA_API_KEY")
BASE_URL = os.getenv("ALIBABA_BASE_URL")
MODEL = os.getenv("ALIBABA_TEXT_MODEL", "qwen-flash")

if not API_KEY or not BASE_URL:
    sys.exit("❌ Brak ALIBABA_API_KEY / ALIBABA_BASE_URL w .env")

prompt = sys.argv[1] if len(sys.argv) > 1 else "Kim jestes? Odpowiedz krotko."
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = requests.post(
    f"{BASE_URL}/chat/completions",
    headers=headers,
    json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    },
    timeout=120,
)

print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"✅ Model: {data['model']}")
    print(data["choices"][0]["message"]["content"])
    print("Tokeny:", data.get("usage"))
else:
    print("Treść:", resp.text)
