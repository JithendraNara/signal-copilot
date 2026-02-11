# Proof Map

| Claim | Evidence | Metric |
|---|---|---|
| Implemented grounded retrieval over local knowledge docs. | `app/retrieval/indexer.py`, `app/retrieval/retriever.py` | Indexed chunk corpus with top-k retrieval |
| Added safe SQL suggestion constrained to approved marts. | `app/sql_guardrails.py` | SQL templates map to 4 approved mart tables |
| Added lightweight evaluation harness for retrieval quality. | `app/api/routes.py` (`/v1/eval`), `data/eval/questions.json` | Pass rate over eval question set |
