"""Orkiestracja rundy debaty."""
import asyncio
from config import MODELS, REVEAL_IDENTITY, USE_CONTEXT, GUARD_FALSE_PREMISE
from adapters import ask


async def run_first_phase(question: str, context: list[dict]) -> list[dict]:
    """Każdy model odpowiada na pytanie niezależnie, równolegle."""

    async def ask_one(model: dict) -> dict:
        system = model["persona"]
        prompt = question

        if USE_CONTEXT and context:
            ctx = _format_context(context)
            guard = (
                "UWAGA: Jeśli kontekst zawiera twierdzenia które wcześniej nie padły "
                "z Twojej strony, zaznacz to wyraźnie zamiast je przyjmować.\n\n"
                if GUARD_FALSE_PREMISE else ""
            )
            prompt = f"Kontekst poprzednich rund:\n{ctx}\n\n{guard}Pytanie: {question}"

        try:
            text = await ask(model["provider"], prompt, system)
            return {"model_id": model["id"], "text": text, "ok": True, "error": None}
        except Exception as e:
            return {"model_id": model["id"], "text": "", "ok": False, "error": str(e)}

    results = await asyncio.gather(*[ask_one(m) for m in MODELS], return_exceptions=False)
    return list(results)


async def run_react_phase(question: str, first_results: list[dict]) -> list[dict]:
    """Każdy model reaguje na odpowiedzi pozostałych, równolegle."""
    first_by_id = {r["model_id"]: r for r in first_results}

    async def ask_one(model: dict) -> dict:
        system = model["persona"]

        # Odpowiedzi innych uczestników
        others = []
        for i, m in enumerate(MODELS, 1):
            if m["id"] == model["id"]:
                continue
            r = first_by_id.get(m["id"])
            if not r or not r.get("ok"):
                continue
            label = m["name"] if REVEAL_IDENTITY else f"Uczestnik {i}"
            others.append(f"{label}:\n{r['text']}")

        own = first_by_id.get(model["id"])
        own_text = own["text"] if own and own.get("ok") else "(brak)"

        others_block = "\n\n---\n\n".join(others) if others else "(brak odpowiedzi od pozostałych)"

        prompt = (
            f"Pytanie debaty: {question}\n\n"
            f"Twoja pierwsza odpowiedź:\n{own_text}\n\n"
            f"Odpowiedzi pozostałych uczestników:\n{others_block}\n\n"
            "Jak reagujesz na powyższe? Możesz się zgodzić, nie zgodzić, "
            "uzupełnić lub zakwestionować stanowisko innych."
        )

        try:
            text = await ask(model["provider"], prompt, system)
            return {"model_id": model["id"], "text": text, "ok": True, "error": None}
        except Exception as e:
            return {"model_id": model["id"], "text": "", "ok": False, "error": str(e)}

    results = await asyncio.gather(*[ask_one(m) for m in MODELS], return_exceptions=False)
    return list(results)


def _format_context(context: list[dict]) -> str:
    parts = []
    for i, rnd in enumerate(context, 1):
        parts.append(f"Runda {i} — pytanie: {rnd.get('question', '?')}")
    return "\n".join(parts)
