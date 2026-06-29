"""Generowanie obrazu przez Together AI (FLUX) -> zapis do output/.

Użycie:
    python image/generate_image.py "opis obrazu"
"""
import base64
import os
import sys
import time

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
load_dotenv(ENV_PATH)

API_KEY = os.getenv("TOGETHER_API_KEY")
BASE_URL = os.getenv("TOGETHER_BASE_URL", "https://api.together.xyz/v1")
MODEL = os.getenv("TOGETHER_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")

if not API_KEY:
    sys.exit("❌ Brak TOGETHER_API_KEY w .env")

prompt = sys.argv[1] if len(sys.argv) > 1 else "a cat astronaut, digital art"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = requests.post(
    f"{BASE_URL}/images/generations",
    headers=headers,
    json={"model": MODEL, "prompt": prompt, "n": 1, "steps": 4},
    timeout=180,
)

print(f"Status: {resp.status_code}")
if resp.status_code != 200:
    sys.exit(f"❌ {resp.text}")

os.makedirs(OUTPUT_DIR, exist_ok=True)
item = resp.json()["data"][0]
fname = os.path.join(OUTPUT_DIR, f"img_{int(time.time())}.png")

if item.get("b64_json"):
    with open(fname, "wb") as f:
        f.write(base64.b64decode(item["b64_json"]))
    print(f"✅ Zapisano: {fname}")
elif item.get("url"):
    img = requests.get(item["url"], timeout=120)
    with open(fname, "wb") as f:
        f.write(img.content)
    print(f"✅ Pobrano i zapisano: {fname}")
else:
    print("⚠️ Nieoczekiwany format odpowiedzi:", item)
