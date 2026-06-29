# AI Research Playground

Lokalny sandbox do testowania wielu dostawców AI z jednego miejsca — przeglądarka + Python CLI.

---

## Jak uruchomić

```bash
pip install flask python-dotenv requests
python3 server.py          # → http://localhost:8080
```

Każdy dostawca ma własny folder z `.env`. Po wklejeniu kluczy:

```bash
python3 make_config.py     # regeneruje keys.json (czytany przez przeglądarkę)
```

Następnie w przeglądarce kliknij **⟳ Odśwież klucze**.

---

## Architektura

```
AI ~Research/
├── index.html          # UI — single-page playground (vanilla JS)
├── server.py           # Flask dev server (port 8080)
│   ├── GET  /          # serwuje index.html
│   ├── GET  /api/providers          # lista folderów z README
│   ├── GET  /api/provider/<name>    # klucz + BASE_URL z .env
│   └── POST /api/add-provider       # tworzy folder + szablony
├── make_config.py      # .env → keys.json  (uruchom po zmianie klucza)
├── keys.json           # [gitignore] klucze dla przeglądarki
│
├── OpenRouter/         # agregator 300+ modeli
├── elevenlabs/         # Text-to-Speech (ElevenLabs API)
├── Groq/               # szybkie LLM inference (Llama, Gemma, Mixtral)
├── MistralAI/          # modele Mistral (Le Chat, Codestral)
├── TogetherAI/         # open-source models + FLUX images
├── Puter/              # browser-only "User Pays" (bez klucza)
├── AlibabaCloud/       # Qwen / DashScope (wymaga weryfikacji)
├── ByteDance/          # Volcengine Ark / Doubao-Seed3D (wymaga konta CN)
└── INNE/               # snippety / eksperymenty
```

### Jak działa UI

1. `initKeys()` — wczytuje `keys.json` → `localStorage`, aktualizuje badge'y na kartach
2. Kliknięcie karty → panel boczny z interfejsem testowym danej platformy
3. **Dynamiczne platformy** (dodane przez formularz) — `loadDynamicProviders()` pobiera `/api/providers`, tworzy kartę i panel z czatem SSE dla każdego folderu z `README.md`
4. OpenRouter — ładuje 300+ modeli live z API, grupuje wg dostawcy, live-search

### Dodawanie nowej platformy (UI)

Kliknij **+ Dodaj Platformę** w gridzie → wpisz nazwę, URL, klucz → `Dodaj`.

Server tworzy `NazwaDostawcy/{scripts,text,output}/`, generuje `README.md`, `.env`, `list_models.py` i `chat.py`. Karta pojawia się w gridzie natychmiast i przeżywa odświeżenie strony.

### Streaming SSE

Panel czatu dynamicznych platform (Groq, Mistral, itd.) używa `stream: true` + `ReadableStream`:
- tokeny pojawiają się natychmiast podczas generowania
- przycisk **■ Stop** przerywa przez `AbortController`
- po zakończeniu pokazywany jest licznik tokenów

---

## Platformy

| Platforma | Typ | Status | Uwagi |
|---|---|---|---|
| **OpenRouter** | LLM agregator | ✅ działa | 300+ modeli, free + paid |
| **ElevenLabs** | TTS | ✅ działa | polskie głosy, streaming audio |
| **Groq** | LLM inference | ✅ działa | ultra-szybki, Llama 3/4, Gemma, Qwen |
| **MistralAI** | LLM | ✅ działa | Mistral Small/Large, Codestral |
| **TogetherAI** | LLM + image | ✅ klucz | chat + FLUX image generation |
| **Puter** | LLM + TTS + img | ✅ bez klucza | User Pays, działa w przeglądarce |
| **AlibabaCloud** | LLM + video | 🔒 zablokowane | oczekuje na weryfikację real-name |
| **ByteDance** | 3D generation | 🔒 brak klucza | wymaga konta Volcengine CN |

---

## Wymagania

```
python >= 3.10
flask
python-dotenv
requests
```

```bash
pip install flask python-dotenv requests
```

---

## Bezpieczeństwo

`keys.json` i wszystkie `.env` są w `.gitignore` — klucze nie trafiają do repo.
Każdy podfolder ma własny `.gitignore` chroniący `.env` i `output/`.
