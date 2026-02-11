from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_ask_and_sql_suggest() -> None:
    ask_res = client.post("/v1/ask", json={"question": "what is conversion_rate?", "top_k": 2})
    assert ask_res.status_code == 200
    assert "Grounded findings" in ask_res.json()["answer"]

    sql_res = client.post("/v1/sql/suggest", json={"question": "show channel performance"})
    assert sql_res.status_code == 200
    body = sql_res.json()
    assert body["safe_sql"] is True
    assert body["table"] == "marts_channel_performance"
