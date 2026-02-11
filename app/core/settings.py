from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = Path(os.getenv("COPILOT_KNOWLEDGE_DIR", BASE_DIR / "data" / "knowledge"))
INDEX_PATH = Path(os.getenv("COPILOT_INDEX_PATH", BASE_DIR / "data" / "knowledge" / "index.json"))
EVAL_PATH = Path(os.getenv("COPILOT_EVAL_PATH", BASE_DIR / "data" / "eval" / "questions.json"))
