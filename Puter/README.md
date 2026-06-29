# Puter (puter.js)

Puter to platforma działająca **w przeglądarce**. Model rozliczeń **„User Pays"**:
to użytkownik końcowy płaci za swoje użycie AI po zalogowaniu — deweloper
**nie potrzebuje klucza API ani serwera**. Stąd brak `.env` i brak Pythona —
wszystko to statyczne pliki HTML/JS.

---

## Struktura katalogu

```
Puter/
├── README.md
└── examples/
    ├── chat.html      # czat z LLM (puter.ai.chat)
    ├── txt2img.html   # generowanie obrazu (puter.ai.txt2img)
    └── tts.html       # text-to-speech + lista silników (puter.ai.txt2speech)
```

> Istniejący folder `INNE/PUTLER/` zawiera wcześniejszy snippet
> (`putler_list.md` — listowanie silników TTS). Te przykłady to jego rozwinięcie.

---

## Jak uruchomić

Puter wymaga kontekstu przeglądarki (nie odpala się z `file://` w pełni
poprawnie z powodu logowania). Najprościej:

```bash
# z katalogu Puter/
python3 -m http.server 8000
# potem otwórz w przeglądarce:
#   http://localhost:8000/examples/chat.html
```

Przy pierwszym wywołaniu AI Puter pokaże **okno logowania** — to normalne
(model „User Pays"). Po zalogowaniu wywołania działają bez żadnego klucza.

---

## Kluczowe API (puter.js v2)

| Funkcja | Wywołanie |
|---|---|
| Czat LLM | `puter.ai.chat(prompt, { model })` |
| Obraz | `puter.ai.txt2img(prompt)` |
| Mowa (TTS) | `puter.ai.txt2speech(text, { voice, engine })` |
| Lista silników TTS | `puter.ai.txt2speech.listEngines('openai')` |

Skrypt SDK: `<script src="https://js.puter.com/v2/"></script>`

---

## Status / blokery

- [x] Brak klucza/serwera — działa od razu w przeglądarce
- [ ] Logowanie użytkownika przy pierwszym wywołaniu (model „User Pays")
