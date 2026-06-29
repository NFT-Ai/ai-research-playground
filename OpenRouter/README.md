# OpenRouter

Agregator modeli AI — jeden klucz API daje dostęp do setek modeli od OpenAI,
Anthropic, Google, Meta, Mistral, DeepSeek i innych. Format OpenAI-compatible.

---

## Struktura katalogu

```
OpenRouter/
├── README.md
├── .env.example           # wzór (OPENROUTER_API_KEY)
├── .gitignore
├── scripts/
│   └── list_models.py     # listowanie modeli / sanity-check
├── text/
│   └── chat.py            # czat (chat/completions)
└── output/
```

---

## Dane platformy

| | Wartość |
|---|---|
| **API base** | `https://openrouter.ai/api/v1` |
| **Klucze API** | https://openrouter.ai/keys |
| **Katalog modeli** | https://openrouter.ai/models |
| **Auth** | `Authorization: Bearer <OPENROUTER_API_KEY>` |
| **Kompatybilność** | OpenAI SDK — podmień tylko `base_url` i klucz |

---

## Szybki start

```bash
cp .env.example .env       # wklej OPENROUTER_API_KEY
pip install requests python-dotenv
python scripts/list_models.py
python text/chat.py "Czesc, kim jestes?"
```

---

## Popularne modele (bezpłatne / tanie)

| Model ID | Opis |
|---|---|
| `google/gemini-flash-1.5` | szybki, tani |
| `meta-llama/llama-3.3-70b-instruct` | Llama 3.3 70B |
| `deepseek/deepseek-chat` | DeepSeek V3 |
| `mistralai/mistral-7b-instruct` | lekki |
| `anthropic/claude-3.5-sonnet` | Sonnet (pay) |
| `openai/gpt-4o-mini` | GPT-4o mini (pay) |

> Modele z `:free` w nazwie (np. `deepseek/deepseek-chat:free`) są darmowe
> z limitami rate. Pełna lista: https://openrouter.ai/models?q=:free

---

## Status / blokery

- [ ] Konto OpenRouter + klucz API
- [ ] `OPENROUTER_API_KEY` wklejony do `.env`

OpenRouter nie wymaga weryfikacji tożsamości — po wklejeniu klucza działa od razu.
Darmowe modele dostępne bez podawania karty.
