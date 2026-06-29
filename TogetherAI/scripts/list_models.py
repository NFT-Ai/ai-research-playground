"""Listowanie modeli Together AI — sanity-check połączenia."""
import os
import sys

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(ENV_PATH)

api_key = os.getenv("TOGETHER_API_KEY")
base_url = os.getenv("TOGETHER_BASE_URL", "https://api.together.xyz/v1")

if not api_key:
    sys.exit("❌ Brak TOGETHER_API_KEY w .env (skopiuj .env.example -> .env).")

headers = {"Authorization": f"Bearer {api_key}"}

try:
    resp = requests.get(f"{base_url}/models", headers=headers, timeout=30)
    print(f"Status: {resp.status_code}")
    resp.raise_for_status()
except requests.exceptions.RequestException as e:
    sys.exit(f"❌ Błąd: {e}\n{getattr(e.response, 'text', '')}")

models = resp.json()
# Together zwraca listę obiektów (czasem pod kluczem 'data')
if isinstance(models, dict):
    models = models.get("data", [])
print(f"✅ Modele ({len(models)}):\n")
for m in sorted(models, key=lambda x: x.get("id", "")):
    print(f"  {m.get('id')}  [{m.get('type', '?')}]")
