REVEAL_IDENTITY = False      # czy modele wiedzą że rozmawiają z innymi AI
USE_CONTEXT = False          # czy przenosić kontekst między rundami
GUARD_FALSE_PREMISE = True   # ochrona przed wszczepioną presupozycją

# Wersje modeli — darmowe tiery (aktualne na 2025-06)
GEMINI_MODEL = "gemini-2.0-flash"          # fallback: gemini-1.5-flash
QWEN_MODEL   = "qwen-plus"                  # fallback: qwen-turbo
GROQ_MODEL   = "llama-3.3-70b-versatile"   # fallback: llama3-70b-8192

MODELS = [
    {
        "id": "alpha",
        "name": "Model α",
        "provider": "gemini",
        "color": "#7C3AED",
        "persona": "Jesteś uczestnikiem otwartej debaty. Odpowiadasz szczerze i bezpośrednio.",
    },
    {
        "id": "beta",
        "name": "Model β",
        "provider": "qwen",
        "color": "#0EA5E9",
        "persona": "Jesteś uczestnikiem otwartej debaty. Odpowiadasz szczerze i bezpośrednio.",
    },
    {
        "id": "gamma",
        "name": "Model γ",
        "provider": "groq",
        "color": "#10B981",
        "persona": "Jesteś uczestnikiem otwartej debaty. Odpowiadasz szczerze i bezpośrednio.",
    },
]
