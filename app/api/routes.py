from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException

from app.core.settings import EVAL_PATH, INDEX_PATH, KNOWLEDGE_DIR
from app.models import AskRequest, AskResponse, EvalResponse, SQLSuggestRequest, SQLSuggestResponse
from app.retrieval.indexer import build_index, load_index
from app.retrieval.retriever import retrieve
from app.sql_guardrails import suggest_sql

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "signal-copilot"}


@router.post("/v1/index/rebuild")
def rebuild_index() -> dict[str, object]:
    docs = build_index(KNOWLEDGE_DIR, INDEX_PATH)
    return {"indexed_chunks": len(docs), "index_path": str(INDEX_PATH)}


@router.post("/v1/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    docs = load_index(INDEX_PATH)
    if not docs:
        docs = build_index(KNOWLEDGE_DIR, INDEX_PATH)

    matches = retrieve(req.question, docs, top_k=req.top_k)
    if not matches:
        raise HTTPException(status_code=404, detail="no grounded context found")

    answer_lines = ["Grounded findings:"]
    for idx, doc in enumerate(matches, start=1):
        answer_lines.append(f"{idx}. {doc['text']}")

    return AskResponse(
        answer="\n".join(answer_lines),
        sources=sorted({m["source"] for m in matches}),
    )


@router.post("/v1/sql/suggest", response_model=SQLSuggestResponse)
def sql_suggest(req: SQLSuggestRequest) -> SQLSuggestResponse:
    return suggest_sql(req.question)


@router.get("/v1/eval", response_model=EvalResponse)
def evaluate() -> EvalResponse:
    docs = load_index(INDEX_PATH)
    if not docs:
        docs = build_index(KNOWLEDGE_DIR, INDEX_PATH)

    if not EVAL_PATH.exists():
        raise HTTPException(status_code=500, detail=f"missing eval set: {EVAL_PATH}")

    tests = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    passed = 0
    for test in tests:
        matches = retrieve(test["question"], docs, top_k=2)
        joined = " ".join(m["text"] for m in matches).lower()
        if test["must_include"].lower() in joined:
            passed += 1

    total = len(tests)
    score = (passed / total) if total else 0.0
    return EvalResponse(total=total, passed=passed, score=round(score, 4))
