# Groq

Ultra-szybki inference LLM — Llama, Gemma, Qwen, Mistral na dedykowanym sprzęcie (LPU).
Format w pełni kompatybilny z OpenAI SDK.

## Dane platformy

| | Wartość |
|---|---|
| **API base** | `https://api.groq.com/openai/v1` |
| **Klucze** | https://console.groq.com/keys |
| **Auth** | `Authorization: Bearer <GROQ_API_KEY>` |
| **Kompatybilność** | OpenAI SDK — podmień tylko `base_url` i klucz |

## Struktura

```
Groq/
├── .env                   # GROQ_API_KEY + GROQ_BASE_URL
├── .env.example
├── .gitignore
├── scripts/
│   └── list_models.py     # lista dostępnych modeli
├── text/
│   └── chat.py            # czat (chat/completions)
└── output/
```

## Szybki start

```bash
cp .env.example .env       # wklej GROQ_API_KEY
pip install requests python-dotenv
python scripts/list_models.py
python text/chat.py "Czesc, kim jestes?"
```

## Modele

| Model ID | Opis | Kontekst |
|---|---|---|
| `llama-3.3-70b-versatile` | Llama 3.3 70B — najlepszy ogólny | 128k |
| `llama-3.1-8b-instant` | Llama 3.1 8B — najszybszy | 128k |
| `llama3-70b-8192` | Llama 3 70B | 8k |
| `gemma2-9b-it` | Google Gemma 2 9B | 8k |
| `qwen-qwq-32b` | Qwen QwQ 32B (reasoning) | 128k |
| `mistral-saba-24b` | Mistral Saba 24B | 32k |
| `compound-beta` | Groq compound model | 128k |

> Pełna lista: `python scripts/list_models.py` lub https://console.groq.com/docs/models

## Cennik

Groq oferuje generous free tier z limitami per minutę/dzień.
Płatne plany od ~$0.05/1M tokenów wejście dla małych modeli.

## Status

- [x] Klucz skonfigurowany
- [x] Połączenie działa
- [x] Panel w przeglądarce — czat ze streamingiem SSE
