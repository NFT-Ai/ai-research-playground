"""Generuje keys.json z plików .env wszystkich platform.

Uruchom po dodaniu nowego klucza:
    python make_config.py

keys.json jest ładowany przez index.html (lokalny serwer).
NIE commituj keys.json do repo.
"""
import json, os
from dotenv import dotenv_values

ROOT = os.path.dirname(__file__)

def env(path, *keys):
    v = dotenv_values(os.path.join(ROOT, path))
    for k in keys:
        val = v.get(k, "")
        if val:
            return val
    return ""

keys = {
    "openrouter":  env("OpenRouter/.env",   "OPENROUTER_API_KEY"),
    "elevenlabs":  env("elevenlabs/.env",    "ELEVENLABS_API_KEY"),
    "alibaba":     env("AlibabaCloud/.env",  "ALIBABA_API_KEY"),
    "alibaba_url": env("AlibabaCloud/.env",  "ALIBABA_BASE_URL"),
    "together":    env("TogetherAI/.env",    "TOGETHER_API_KEY"),
    "bytedance":   env("ByteDance/.env",     "ARK_API_KEY"),
        "groq":  env("Groq/.env", "GROQ_API_KEY"),
        "mistralai":  env("MistralAI/.env", "MISTRALAI_API_KEY"),
        "cerebras":  env("Cerebras/.env", "CEREBRAS_API_KEY"),
}

out = os.path.join(ROOT, "keys.json")
with open(out, "w") as f:
    json.dump(keys, f, indent=2)

for k, v in keys.items():
    status = f"✅ {v[:12]}…" if v else "⬜ brak"
    print(f"  {k:<14} {status}")
print(f"\n→ Zapisano: {out}")
