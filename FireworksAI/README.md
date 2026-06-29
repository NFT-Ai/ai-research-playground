# FireworksAI

## Dane platformy
| | Wartość |
|---|---|
| **API base** | `https://api.fireworks.ai/inference/v1` |
| **Auth** | `Authorization: Bearer <FIREWORKSAI_API_KEY>` |
| **Typy** | Text · Image · Video · Audio |

## Szybki start
```bash
cp .env.example .env   # uzupełnij FIREWORKSAI_API_KEY
pip install requests python-dotenv
python scripts/list_models.py
python text/chat.py "Twoje pytanie"
```

## Status
- [ ] Klucz API skonfigurowany (FIREWORKSAI_API_KEY w .env)
- [ ] Połączenie zweryfikowane
