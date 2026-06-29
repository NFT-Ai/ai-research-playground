"""Czat z modelem Together AI (chat/completions, format OpenAI).

Użycie:
    python text/chat.py "Twoje pytanie"
"""
import os
import sys

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(ENV_PATH)

API_KEY = os.getenv("TOGETHER_API_KEY")
BASE_URL = os.getenv("TOGETHER_BASE_URL", "https://api.together.xyz/v1")
MODEL = os.getenv("TOGETHER_TEXT_MODEL", "meta-llama/Llama-3.3-70B-Instruct-Turbo")

if not API_KEY:
    sys.exit("❌ Brak TOGETHER_API_KEY w .env")

prompt = sys.argv[1] if len(sys.argv) > 1 else "Czesc, kim jestes?"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = requests.post(
    f"{BASE_URL}/chat/completions",
    headers=headers,
    json={"model": MODEL, "messages": [{"role": "user", "content": prompt}]},
    timeout=120,
)

print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"✅ Model: {data.get('model')}")
    print(data["choices"][0]["message"]["content"])
    print("Tokeny:", data.get("usage"))
else:
    print("Treść:", resp.text)
