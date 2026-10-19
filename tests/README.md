# Tests

The folders here follow the structure of `src/`.

| Folder | Tool | Run |
| --- | --- | --- |
| `backend/` | pytest | `pytest tests/backend` |
| `speech_service/` | pytest | `pytest tests/speech_service` |
| `llm_service/` | pytest | `pytest tests/llm_service` |
| `frontend/` | Vitest | `cd src/frontend && npm test` |
| `e2e/` | end-to-end scenarios | later |
| `fixtures/` | small fake test data | |

Rule: tests use **fake data only**. No real student names, answers or voice recordings.
