"""Czat przez OpenRouter (OpenAI-compatible).

Użycie:
    python text/chat.py "Twoje pytanie"
    python text/chat.py "Pytanie" --model anthropic/claude-3.5-sonnet
"""
import os
import sys

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(ENV_PATH)

API_KEY  = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
MODEL    = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat:free")

if not API_KEY:
    sys.exit("❌ Brak OPENROUTER_API_KEY w .env")

args   = sys.argv[1:]
prompt = args[0] if args and not args[0].startswith("--") else "Czesc, kim jestes? Odpowiedz krotko."
if "--model" in args:
    MODEL = args[args.index("--model") + 1]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",   # wymagane przez OpenRouter
}

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
