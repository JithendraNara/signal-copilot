from __future__ import annotations

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=3, ge=1, le=8)


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


class SQLSuggestRequest(BaseModel):
    question: str = Field(min_length=3)


class SQLSuggestResponse(BaseModel):
    sql: str
    table: str
    safe_sql: bool
    rationale: str


class EvalResponse(BaseModel):
    total: int
    passed: int
    score: float
