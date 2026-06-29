"""Listowanie modeli z Alibaba Cloud Model Studio — sanity-check połączenia."""
import os
import sys

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(ENV_PATH)

api_key = os.getenv("ALIBABA_API_KEY")
base_url = os.getenv("ALIBABA_BASE_URL")

if not api_key or not base_url:
    sys.exit("❌ Brak ALIBABA_API_KEY / ALIBABA_BASE_URL w .env")

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

try:
    resp = requests.get(f"{base_url}/models", headers=headers, timeout=30)
    print(f"Status: {resp.status_code}")
    resp.raise_for_status()
except requests.exceptions.RequestException as e:
    sys.exit(f"❌ Błąd: {e}\n{getattr(e.response, 'text', '')}")

models = resp.json().get("data", [])
print(f"✅ Dostępne modele ({len(models)}):\n")
for m in sorted(models, key=lambda x: x.get("id", "")):
    print(f"  {m['id']}")
