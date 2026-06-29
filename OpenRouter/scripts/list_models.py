"""Listowanie modeli OpenRouter — sanity-check połączenia.

Użycie:
    python scripts/list_models.py           # wszystkie modele
    python scripts/list_models.py free      # tylko darmowe (:free)
    python scripts/list_models.py deepseek  # filtr po nazwie
"""
import os
import sys

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(ENV_PATH)

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    sys.exit("❌ Brak OPENROUTER_API_KEY w .env (skopiuj .env.example -> .env).")

filtr = sys.argv[1].lower() if len(sys.argv) > 1 else ""

try:
    resp = requests.get(f"{base_url}/models",
                        headers={"Authorization": f"Bearer {api_key}"},
                        timeout=30)
    print(f"Status: {resp.status_code}")
    resp.raise_for_status()
except requests.exceptions.RequestException as e:
    sys.exit(f"❌ Błąd: {e}")

models = resp.json().get("data", [])
if filtr:
    models = [m for m in models if filtr in m.get("id", "").lower()]

print(f"✅ Modeli: {len(models)}\n")
for m in sorted(models, key=lambda x: x.get("id", "")):
    ctx = m.get("context_length", "?")
    price_in  = m.get("pricing", {}).get("prompt", "?")
    price_out = m.get("pricing", {}).get("completion", "?")
    print(f"  {m['id']:<55} ctx:{ctx:>7}  in:{price_in} out:{price_out}")
