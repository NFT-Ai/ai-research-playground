"""
FastAPI — serwuje frontend i pośredniczy w wywołaniach do modeli LLM.

Uruchomienie:
    uvicorn main:app --reload --port 8000

Endpointy:
    GET  /           → static/index.html
    POST /api/ask    → jedno pytanie do jednego modelu
    POST /api/debate → pełna runda debaty (fazy: first, react)
    GET  /api/models → lista modeli z config.py (do info w UI)
"""
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()  # wczytaj .env zanim cokolwiek zaimportuje os.environ

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from config import MODELS
from adapters import ask as ask_adapter
from debate import run_first_phase, run_react_phase

app = FastAPI(title="Debata Modeli")
STATIC = Path(__file__).parent / "static"


# ── Static ────────────────────────────────────────────────────────────────────
@app.get("/")
async def index():
    return FileResponse(STATIC / "index.html")


# ── Config ────────────────────────────────────────────────────────────────────
@app.get("/api/models")
async def get_models():
    return [{"id": m["id"], "name": m["name"], "color": m["color"]} for m in MODELS]


# ── /api/ask ──────────────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    model_id: str
    prompt: str
    system: str = ""


@app.post("/api/ask")
async def api_ask(req: AskRequest):
    model = next((m for m in MODELS if m["id"] == req.model_id), None)
    if not model:
        return {"model_id": req.model_id, "text": "", "ok": False,
                "error": f"Nieznany model: {req.model_id!r}"}
    try:
        text = await ask_adapter(model["provider"], req.prompt,
                                 req.system or model["persona"])
        return {"model_id": req.model_id, "text": text, "ok": True, "error": None}
    except Exception as e:
        return {"model_id": req.model_id, "text": "", "ok": False, "error": str(e)}


# ── /api/debate ───────────────────────────────────────────────────────────────
class DebateRequest(BaseModel):
    question: str
    context: list = []
    phases: list[str] = ["first", "react"]
    first_results: list[dict] = []   # wypełnione przez frontend przy fazie react


@app.post("/api/debate")
async def api_debate(req: DebateRequest):
    result: dict = {"question": req.question}
    first_results = req.first_results  # może być puste

    if "first" in req.phases:
        first_results = await run_first_phase(req.question, req.context)
        result["first"] = first_results

    if "react" in req.phases:
        if not first_results:
            result["react"] = [
                {"model_id": m["id"], "text": "", "ok": False,
                 "error": "Brak wyników fazy 'first' — wywołaj najpierw fazę first."}
                for m in MODELS
            ]
        else:
            result["react"] = await run_react_phase(req.question, first_results)

    return result
