"""
Adaptery do trzech dostawców LLM.
Każdy eksportuje async ask(prompt, system) -> str.
Klucze tylko z os.environ — nigdy w kodzie.

Linki do dokumentacji:
  Gemini:  https://ai.google.dev/api/generate-content
  Qwen:    https://www.alibabacloud.com/help/en/model-studio/developer-reference/use-qwen-by-calling-api
  Groq:    https://console.groq.com/docs/openai
"""
import os
import httpx
from openai import AsyncOpenAI

from config import GEMINI_MODEL, QWEN_MODEL, GROQ_MODEL


# ── Gemini ────────────────────────────────────────────────────────────────────
# Format NIE jest OpenAI-compatible — własny schemat Googla.
# Klucz w query stringu (?key=...).
async def ask_gemini(prompt: str, system: str) -> str:
    api_key = os.environ["GEMINI_API_KEY"]
    model   = os.environ.get("GEMINI_MODEL", GEMINI_MODEL)
    url     = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system}]},
        "generationConfig": {"maxOutputTokens": 1024},
    }
    async with httpx.AsyncClient(timeout=45) as client:
        r = await client.post(url, params={"key": api_key}, json=body)
        r.raise_for_status()
        data = r.json()

    # Gemini zwraca: candidates[0].content.parts[0].text
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        raise ValueError(f"Nieoczekiwany format odpowiedzi Gemini: {data}") from e


# ── Qwen (OpenAI-compatible, endpoint EU) ────────────────────────────────────
# Endpoint międzynarodowy (EU) — NIE używaj klucza z workspace cn-beijing.
# Klucz z konsoli Alibaba Cloud Model Studio (international).
async def ask_qwen(prompt: str, system: str) -> str:
    client = AsyncOpenAI(
        api_key=os.environ["QWEN_API_KEY"],
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )
    model = os.environ.get("QWEN_MODEL", QWEN_MODEL)
    r = await client.chat.completions.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
    )
    return r.choices[0].message.content


# ── Groq (OpenAI-compatible) ─────────────────────────────────────────────────
# Najszybszy z trzech — dobry do testowania.
async def ask_groq(prompt: str, system: str) -> str:
    client = AsyncOpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )
    model = os.environ.get("GROQ_MODEL", GROQ_MODEL)
    r = await client.chat.completions.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
    )
    return r.choices[0].message.content


# ── Dispatcher ────────────────────────────────────────────────────────────────
_ADAPTERS = {
    "gemini": ask_gemini,
    "qwen":   ask_qwen,
    "groq":   ask_groq,
}


async def ask(provider: str, prompt: str, system: str) -> str:
    fn = _ADAPTERS.get(provider)
    if not fn:
        raise ValueError(f"Nieznany provider: {provider!r}")
    return await fn(prompt, system)
