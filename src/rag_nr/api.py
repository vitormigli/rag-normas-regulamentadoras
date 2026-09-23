"""FastAPI service exposing POST /ask over the ingested NRs."""

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

from rag_nr.generation import answer_question  # noqa: E402

app = FastAPI(title="RAG — Normas Regulamentadoras")


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask")
def ask(req: AskRequest) -> dict:
    answer, chunks = answer_question(req.question, top_k=req.top_k)
    return {
        "answer": answer.text,
        "sources": [
            {"norma": c["norma"], "item": c["item"], "pagina": c["pagina"]} for c in chunks
        ],
    }
