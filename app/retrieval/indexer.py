from __future__ import annotations

import json
from pathlib import Path



def _chunk_text(content: str) -> list[str]:
    parts = [p.strip() for p in content.split("\n\n") if p.strip()]
    return [p for p in parts if len(p) > 25]


def build_index(knowledge_dir: Path, out_path: Path) -> list[dict[str, str]]:
    docs: list[dict[str, str]] = []
    for path in sorted(knowledge_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        for idx, chunk in enumerate(_chunk_text(content), start=1):
            docs.append(
                {
                    "id": f"{path.name}:{idx}",
                    "source": path.name,
                    "text": chunk,
                }
            )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(docs, indent=2), encoding="utf-8")
    return docs


def load_index(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))
