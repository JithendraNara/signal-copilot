from __future__ import annotations

from difflib import SequenceMatcher
import re
from collections import Counter


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_]+", text.lower())


def _overlap_score(query: str, text: str) -> float:
    q = Counter(_tokenize(query))
    t = Counter(_tokenize(text))
    if not q:
        return 0.0
    overlap = sum((q & t).values())
    return overlap / max(sum(q.values()), 1)


def score_document(query: str, doc_text: str) -> float:
    lexical = _overlap_score(query, doc_text)
    fuzzy = SequenceMatcher(None, query.lower(), doc_text.lower()).ratio()
    return 0.65 * lexical + 0.35 * fuzzy


def retrieve(query: str, docs: list[dict[str, str]], top_k: int = 3) -> list[dict[str, str]]:
    ranked = sorted(
        docs,
        key=lambda d: score_document(query, d["text"]),
        reverse=True,
    )
    return ranked[:top_k]
