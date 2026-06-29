"""Sanity-check połączenia z Volcengine Ark — listuje modele / weryfikuje klucz.

Uzupełnij ARK_API_KEY w ../.env i uruchom:
    python scripts/list_models.py
"""
import os
import sys

import requests
from dotenv import load_dotenv

# .env leży w katalogu ByteDance/ (poziom wyżej niż scripts/)
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(ENV_PATH)

api_key = os.getenv("ARK_API_KEY")
base_url = os.getenv("ARK_BASE_URL")

if not api_key:
    sys.exit("❌ Brak ARK_API_KEY w .env (skopiuj .env.example -> .env i uzupełnij).")

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

try:
    resp = requests.get(f"{base_url}/models", headers=headers, timeout=30)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        models = resp.json().get("data", [])
        print(f"✅ Połączenie OK. Modeli: {len(models)}")
        for m in sorted(models, key=lambda x: x.get("id", "")):
            print(f"  {m.get('id')}")
    else:
        print("Treść odpowiedzi:", resp.text[:300])
except requests.exceptions.RequestException as e:
    sys.exit(f"❌ Błąd połączenia: {e}")
