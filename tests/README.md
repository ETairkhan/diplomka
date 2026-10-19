# Tests

The folders here follow the structure of `src/`.

| Folder | Tool | Run |
| --- | --- | --- |
| `backend/` | Go `testing` (API tests) | `cd tests/backend && go test ./...` |
| `ml_service/` | pytest | `pytest` (from the repository root) |
| `frontend/` | Vitest | `cd src/frontend && npm test` |
| `e2e/` | end-to-end scenarios | later |
| `fixtures/` | small fake test data | |

Go unit tests are also next to the code (`src/backend/**/*_test.go`), as is usual in Go:
`cd src/backend && go test ./...`

Rule: tests use **fake data only**. No real student names, answers or voice recordings.
