# Debata Modeli Językowych

Trzy modele AI (Gemini α · Qwen β · Groq γ) odpowiadają na to samo pytanie niezależnie,
potem reagują na swoje wzajemne odpowiedzi. Jeden serwer FastAPI serwuje frontend i
pośredniczy w wywołaniach do API — brak CORS, brak CSP, brak build-stepu.

---

## Architektura

```
Przeglądarka (static/index.html)
      │  fetch('/api/...') — ten sam origin, zero CORS
      ▼
FastAPI (main.py, port 8000)
      ├── GET  /              → static/index.html
      ├── POST /api/ask       → jedno pytanie do jednego modelu
      └── POST /api/debate    → pełna runda (fazy: first + react)
            ├── adapters.py   → Gemini | Qwen | Groq (równoległe asyncio.gather)
            └── debate.py     → orkiestracja, prompty, obsługa błędów per-model
```

## Uruchomienie lokalne (macOS)

```bash
cd debata
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# → uzupełnij klucze w .env (patrz niżej)

uvicorn main:app --reload --port 8000
# otwórz http://localhost:8000
```

## Klucze API (darmowe tiery)

Wpisz do `.env` (NIE do `.env.example`, `.env` jest w `.gitignore`):

| Zmienna | Skąd wziąć |
|---|---|
| `GEMINI_API_KEY` | https://aistudio.google.com/apikey |
| `QWEN_API_KEY` | Alibaba Cloud Model Studio → International workspace → API Keys |
| `GROQ_API_KEY` | https://console.groq.com/keys |

> **Uwaga Qwen**: użyj klucza z workspace **EU/International**
> (`dashscope-intl.aliyuncs.com`), NIE klucza z workspace cn-beijing.

## Szybki test curl

```bash
# Test Groq (najszybszy)
curl -s -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"model_id":"gamma","prompt":"Czym jest świadomość? Odpowiedz w 2 zdaniach."}' | python3 -m json.tool

# Test pełnej rundy
curl -s -X POST http://localhost:8000/api/debate \
  -H "Content-Type: application/json" \
  -d '{"question":"Czy AI może być twórcza?","phases":["first"]}' | python3 -m json.tool
```

## Konfiguracja (`config.py`)

| Flaga | Domyślnie | Opis |
|---|---|---|
| `REVEAL_IDENTITY` | `False` | Modele widzą się nawzajem jako "Uczestnik N", nie jako AI |
| `USE_CONTEXT` | `False` | Każda runda niezależna (włącz dla eksperymentów z kontekstem) |
| `GUARD_FALSE_PREMISE` | `True` | Przed pytaniem z kontekstem: instrukcja anty-sycophancy |

## Wdrożenie na VPS (Traefik + Docker)

```bash
# Na VPS (Hostinger KVM)
git clone <repo> && cd debata
cp .env.example .env && nano .env   # uzupełnij klucze

docker compose up -d
# → dostępne pod https://debata.srv1041521.hstgr.cloud
```

Wymagania VPS:
- Docker + Docker Compose
- Działający Traefik z entrypointem `websecure` i certresolver `letsencrypt`
- Sieć zewnętrzna `web` (`docker network create web`)

## Struktura plików

```
debata/
├── .env.example        # wzór kluczy
├── .gitignore          # chroni .env + __pycache__
├── requirements.txt
├── config.py           # modele, flagi eksperymentalne
├── adapters.py         # Gemini + Qwen + Groq
├── debate.py           # logika faz first/react
├── main.py             # FastAPI routing
├── static/
│   └── index.html      # cały frontend (vanilla JS, zero dependencji)
├── Dockerfile
└── docker-compose.yml
```
