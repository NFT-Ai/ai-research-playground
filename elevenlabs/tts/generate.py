"""Generowanie audio ElevenLabs → output/

Użycie:
    python tts/generate.py "Tekst do syntezy"
    python tts/generate.py "Tekst" --voice "Michał Lubaszewski - PL" --model eleven_multilingual_v2
"""
import os, sys, time
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "output")

API_KEY = os.getenv("ELEVENLABS_API_KEY")
BASE    = "https://api.elevenlabs.io/v1"

if not API_KEY:
    sys.exit("❌ Brak ELEVENLABS_API_KEY w .env")

# domyślny głos: Michał Lubaszewski PL
DEFAULT_VOICE = "ynIo8Bwfrnj9CiMSjKZM"
DEFAULT_MODEL = "eleven_multilingual_v2"

def get_voice_id(name: str) -> str:
    r = requests.get(f"{BASE}/voices", headers={"xi-api-key": API_KEY}, timeout=15)
    r.raise_for_status()
    for v in r.json()["voices"]:
        if name.lower() in v["name"].lower():
            return v["voice_id"]
    sys.exit(f"❌ Głos '{name}' nie znaleziony. Użyj scripts/list_voices.py aby zobaczyć listę.")

args   = sys.argv[1:]
text   = args[0] if args and not args[0].startswith("--") else "Cześć, to jest test polskiej syntezy mowy."
voice_name = None
model  = DEFAULT_MODEL

if "--voice" in args:
    voice_name = args[args.index("--voice") + 1]
if "--model" in args:
    model = args[args.index("--model") + 1]

voice_id = get_voice_id(voice_name) if voice_name else DEFAULT_VOICE

print(f"▶ Tekst: {text}")
print(f"▶ Głos ID: {voice_id}  Model: {model}")

r = requests.post(
    f"{BASE}/text-to-speech/{voice_id}",
    headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
    json={"text": text, "model_id": model, "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}},
    timeout=60,
)
r.raise_for_status()
os.makedirs(OUTPUT, exist_ok=True)
fname = os.path.join(OUTPUT, f"el_{int(time.time())}.mp3")
with open(fname, "wb") as f:
    f.write(r.content)
print(f"✅ Zapisano: {fname}")
