# MistralAI

Europejski dostawca LLM — modele Mistral Small, Large, Codestral (kod).
Format kompatybilny z OpenAI SDK.

## Dane platformy

| | Wartość |
|---|---|
| **API base** | `https://api.mistral.ai/v1` |
| **Klucze** | https://console.mistral.ai/api-keys |
| **Auth** | `Authorization: Bearer <MISTRALAI_API_KEY>` |
| **Kompatybilność** | OpenAI SDK — podmień tylko `base_url` i klucz |

## Struktura

```
MistralAI/
├── .env                   # MISTRALAI_API_KEY + MISTRALAI_BASE_URL
├── .env.example
├── .gitignore
├── scripts/
│   └── list_models.py     # lista modeli
├── text/
│   └── chat.py            # czat (chat/completions)
└── output/
```

## Szybki start

```bash
cp .env.example .env       # wklej MISTRALAI_API_KEY
pip install requests python-dotenv
python scripts/list_models.py
python text/chat.py "Czesc, kim jestes?"
```

## Modele

| Model ID | Opis | Kontekst |
|---|---|---|
| `mistral-small-latest` | Szybki, tani model ogólny | 32k |
| `mistral-medium-latest` | Balans jakość/cena | 32k |
| `mistral-large-latest` | Najlepszy model Mistral | 128k |
| `codestral-latest` | Specjalizowany do kodu | 32k |
| `open-mistral-7b` | Open-source 7B | 32k |
| `open-mixtral-8x7b` | Open-source MoE 8x7B | 32k |

> Pełna lista: `python scripts/list_models.py`

## Cennik

- Mistral Small: ~$0.20/1M tokenów wejście
- Mistral Large: ~$2.00/1M tokenów wejście
- Codestral: ~$0.20/1M tokenów wejście

## Status

- [x] Klucz skonfigurowany
- [x] Panel w przeglądarce — czat ze streamingiem SSE
- [ ] Połączenie zweryfikowane
