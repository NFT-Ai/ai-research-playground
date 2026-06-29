"""Czat z Groq (OpenAI-compatible).

Użycie:
    python text/chat.py "Twoje pytanie"
"""
import os, sys
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
API_KEY  = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
MODEL    = os.getenv("GROQ_MODEL", "")

if not API_KEY:
    sys.exit("❌ Brak GROQ_API_KEY w .env")

prompt = sys.argv[1] if len(sys.argv) > 1 else "Czesc, kim jestes? Odpowiedz krotko."
if not MODEL:
    print("⚠️  Brak GROQ_MODEL w .env — wpisz model jako drugi argument lub uzupełnij .env")
    MODEL = sys.argv[2] if len(sys.argv) > 2 else ""
    if not MODEL:
        sys.exit("❌ Podaj nazwę modelu jako sys.argv[2] lub ustaw GROQ_MODEL w .env")

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
r = requests.post(f"{BASE_URL}/chat/completions", headers=headers,
    json={"model": MODEL, "messages": [{"role": "user", "content": prompt}]},
    timeout=120)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    d = r.json()
    print(f"✅ Model: {d.get('model')}")
    print(d["choices"][0]["message"]["content"])
    print("Tokeny:", d.get("usage"))
else:
    print("Treść:", r.text[:400])
