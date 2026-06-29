"""Listowanie modeli Cerebras — sanity-check połączenia."""
import os, sys
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
api_key  = os.getenv("CEREBRAS_API_KEY")
base_url = os.getenv("CEREBRAS_BASE_URL", "https://api.cerebras.ai/v1")

if not api_key:
    sys.exit("❌ Brak CEREBRAS_API_KEY w .env (skopiuj .env.example → .env).")

headers = {"Authorization": f"Bearer {api_key}"}

try:
    r = requests.get(f"{base_url}/models", headers=headers, timeout=30)
    print(f"Status: {r.status_code}")
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    sys.exit(f"❌ Błąd: {e}\n{getattr(e.response,'text','')[:200]}")

data = r.json()
models = data if isinstance(data, list) else data.get("data", [])
print(f"✅ Modeli: {len(models)}\n")
for m in sorted(models, key=lambda x: x.get("id", x.get("name", ""))):
    print(f"  {m.get('id', m.get('name', m))}")
