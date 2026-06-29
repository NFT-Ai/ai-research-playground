"""Lista wszystkich głosów ElevenLabs dla konta."""
import os, sys
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
key = os.getenv("ELEVENLABS_API_KEY")
if not key:
    sys.exit("❌ Brak ELEVENLABS_API_KEY w .env")

r = requests.get("https://api.elevenlabs.io/v1/voices",
    headers={"xi-api-key": key}, timeout=15)
r.raise_for_status()
voices = sorted(r.json()["voices"], key=lambda x: x["name"])
print(f"✅ Głosy ({len(voices)}):\n")
for v in voices:
    pl = " ← PL" if any(x in v["name"] for x in ["PL","Michał","Piotr","Aleksandra","kAImil","Bartlomiej","WKW","Lubaszewski","Fronczewski"]) else ""
    print(f"  {v['name']:<40} {v['voice_id']}  [{v.get('category','?')}]{pl}")
