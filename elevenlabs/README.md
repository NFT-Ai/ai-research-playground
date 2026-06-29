# ElevenLabs

Text-to-Speech API. Klucz skonfigurowany i zweryfikowany — działa.

## Struktura
```
elevenlabs/
├── .env                   # klucze (ELEVENLABS_API_KEY)
├── .env.example
├── .gitignore
├── scripts/list_voices.py # lista wszystkich głosów
├── tts/generate.py        # generacja audio → output/
└── output/
```

## Dane platformy
| | Wartość |
|---|---|
| **API base** | `https://api.elevenlabs.io/v1` |
| **Auth header** | `xi-api-key: <ELEVENLABS_API_KEY>` |
| **Klucze** | https://elevenlabs.io/app/settings/api-keys |

## Szybki start
```bash
pip install requests python-dotenv
python scripts/list_voices.py
python tts/generate.py "Cześć, to jest test." --voice "Michał Lubaszewski - PL"
```

## Modele
| Model ID | Opis |
|---|---|
| `eleven_multilingual_v2` | najlepsza jakość, multi-język |
| `eleven_turbo_v2_5` | szybki, tani |
| `eleven_flash_v2_5` | najszybszy, najniższy koszt |

## Polskie głosy (professional)
- `Michał Lubaszewski - PL` — ynIo8Bwfrnj9CiMSjKZM
- `Piotr Fronczewski™` — T5l58N8RNz5DKoClpKIJ
- `Konwersacyjny kAImil` — mr1ubFaLs5xVrh1EqWtc
- `Uprzejma Aleksandra` — 8EWWaNTDrqObI22Gvo1q
- `Bartlomiej – Universal Power` — mE4ZaAjuN2kFvhpzKG06
- `WKW - Warm & Calm Storyteller` — h83JI5fjWWu9AOKOVRYh
