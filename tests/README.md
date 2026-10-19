# Tests

The folders here follow the structure of `src/`.

| Folder | Tool | Run |
| --- | --- | --- |
| `backend/` | Go `testing` (API tests) | `cd tests/backend && go test ./...` |
| `speech_service/` | pytest | `pytest tests/speech_service` |
| `llm_service/` | pytest | `pytest tests/llm_service` |
| `frontend/` | Vitest | `cd src/frontend && npm test` |
| `e2e/` | end-to-end scenarios | later |
| `fixtures/` | small fake test data | |

Go unit tests are also next to the code (`src/backend/**/*_test.go`), as is usual in Go:
`cd src/backend && go test ./...`

Rule: tests use **fake data only**. No real student names, answers or voice recordings.
