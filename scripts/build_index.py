from __future__ import annotations

from app.core.settings import INDEX_PATH, KNOWLEDGE_DIR
from app.retrieval.indexer import build_index


if __name__ == "__main__":
    docs = build_index(KNOWLEDGE_DIR, INDEX_PATH)
    print(f"Indexed {len(docs)} chunks into {INDEX_PATH}")
