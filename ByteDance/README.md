# ByteDance — Volcengine Ark (Doubao)

Struktura przygotowana **na przyszłość**. Wszystko gotowe do działania, gdy
zdobędziesz **API Key** z Volcengine Ark i model zostanie aktywowany.

> ⚠️ Volcengine to chmura *mainland China*. Wymaga konta + weryfikacji tożsamości
> (real-name), zwykle z chińskim numerem/dokumentem. To główny bloker dla kont
> spoza Chin — patrz sekcja „Status / blokery" niżej.

---

## Struktura katalogu

```
ByteDance/
├── README.md              # ten plik
├── .env.example           # wzór konfiguracji (skopiuj do .env i uzupełnij)
├── .gitignore             # chroni .env z prawdziwym kluczem
├── seed3d/                # generowanie 3D (doubao-seed3d-2-0)
│   └── generate_3d.py     # szkielet skryptu text/image → 3D
├── scripts/               # narzędzia pomocnicze
│   └── list_models.py     # listowanie / sanity-check połączenia
└── output/                # tu trafiają wygenerowane pliki (3D, podgląd)
```

---

## Dane platformy

| | Wartość |
|---|---|
| **Konsola** | https://console.volcengine.com/ark |
| **Ark API base** | `https://ark.cn-beijing.volces.com/api/v3` |
| **Model 3D** | `doubao-seed3d-2-0` (Seed3D 2.0) |
| **Region** | `cn-beijing` |
| **Auth** | `Authorization: Bearer <ARK_API_KEY>` |

> Endpoint i dokładny kształt zapytania dla Seed3D należy potwierdzić w
> dokumentacji Ark po uzyskaniu dostępu — Ark bywa zmienny. Szkielet w
> `seed3d/generate_3d.py` zakłada wzorzec async (submit → polling → URL).

---

## Szybki start (gdy będzie klucz)

```bash
cp .env.example .env          # wklej ARK_API_KEY
pip install requests python-dotenv
python scripts/list_models.py # sanity-check połączenia
python seed3d/generate_3d.py  # generacja 3D
```

---

## Status / blokery

- [ ] Konto Volcengine założone
- [ ] Weryfikacja tożsamości (real-name) zakończona
- [ ] Model `doubao-seed3d-2-0` aktywowany w Ark
- [ ] `ARK_API_KEY` utworzony i wklejony do `.env`
- [ ] Potwierdzony format API Seed3D w dokumentacji

Dopóki powyższe nie jest spełnione, wywołania zwrócą błąd dostępu/weryfikacji
(analogicznie do Alibaby: `AccessDenied` / `NO_REAL_REGISTER_AUTHENTICATION`).
