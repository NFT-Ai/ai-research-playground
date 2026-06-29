# Together AI

REST API kompatybilne z OpenAI. Hosting wielu modeli open-source (Llama, Qwen,
DeepSeek, FLUX itd.). Wymaga klucza API.

---

## Struktura katalogu

```
TogetherAI/
├── README.md
├── .env.example           # wzór (TOGETHER_API_KEY, TOGETHER_BASE_URL)
├── .gitignore
├── scripts/
│   └── list_models.py     # listowanie modeli / sanity-check
├── text/
│   └── chat.py            # czat (chat/completions)
├── image/
│   └── generate_image.py  # generowanie obrazów (FLUX) -> output/
└── output/
```

---

## Dane platformy

| | Wartość |
|---|---|
| **API base** | `https://api.together.xyz/v1` |
| **Konsola / klucze** | https://api.together.ai/settings/api-keys |
| **Auth** | `Authorization: Bearer <TOGETHER_API_KEY>` |
| **Kompatybilność** | OpenAI SDK (wystarczy podmienić `base_url`) |

> `api.together.ai` i `api.together.xyz` wskazują tę samą usługę; w wywołaniach
> API kanoniczny jest `https://api.together.xyz/v1`.

---

## Szybki start

```bash
cp .env.example .env       # wklej TOGETHER_API_KEY
pip install requests python-dotenv
python scripts/list_models.py
python text/chat.py "Czesc, kim jestes?"
python image/generate_image.py "a cat astronaut, digital art"
```

---

## Status / blokery

- [ ] Konto Together AI + klucz API
- [ ] `TOGETHER_API_KEY` wklejony do `.env`

Together zwykle nie wymaga weryfikacji tożsamości jak chmury chińskie —
po wklejeniu klucza skrypty powinny zadziałać od razu (model pay-as-you-go).
