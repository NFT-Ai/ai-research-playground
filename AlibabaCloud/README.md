# Alibaba Cloud — Model Studio (Qwen / DashScope)

Struktura analogiczna do `ByteDance/`. Połączenie i klucz **działają**
(listowanie modeli zwraca 200), ale wywołania modeli są zablokowane do czasu
**weryfikacji tożsamości konta** — patrz „Status / blokery".

---

## Struktura katalogu

```
AlibabaCloud/
├── README.md              # ten plik
├── .env                   # prawdziwy klucz (region Pekin) — NIE commitować
├── .env.example           # wzór konfiguracji
├── .gitignore             # chroni .env + output/
├── scripts/
│   └── list_models.py     # listowanie modeli / sanity-check
├── text/
│   └── chat.py            # czat (OpenAI-compatible) — qwen-flash itd.
├── video/
│   └── generate_video.py  # async text→video (happyhorse-1.1-t2v, DashScope)
└── output/                # wyniki
```

---

## Dane platformy (aktualny region: Pekin)

| | Wartość |
|---|---|
| **OpenAI-compatible** | `https://ws-kjcudg5llgx0q5mj.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| **DashScope** | `https://ws-kjcudg5llgx0q5mj.cn-beijing.maas.aliyuncs.com/api/v1` |
| **Region** | `cn-beijing` |
| **Auth** | `Authorization: Bearer <ALIBABA_API_KEY>` |

> Klucze są **specyficzne dla regionu/workspace** — klucz pekiński nie zadziała
> na endpointcie frankfurckim (i odwrotnie). To była przyczyna wcześniejszego 401.

---

## Szybki start

```bash
pip install requests python-dotenv
python scripts/list_models.py     # ✅ działa już teraz (200)
python text/chat.py "Czesc"       # 🔒 do odblokowania po weryfikacji
python video/generate_video.py    # 🔒 do odblokowania po weryfikacji
```

---

## Status / blokery

- [x] Konto + klucz API (region Pekin)
- [x] Połączenie działa (`/models` → 200, 165 modeli)
- [ ] **Weryfikacja tożsamości (real-name)** — blokuje wszystkie wywołania
- [ ] Aktywacja / billing modeli

Dopóki weryfikacja nie jest gotowa, wywołania zwracają:
`403 AccessDenied.Unpurchased` lub `NO_REAL_REGISTER_AUTHENTICATION`.
Kod jest poprawny — blokada jest czysto kontowa.
