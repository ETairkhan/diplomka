# Backend (Go)

Main REST API. It handles users and roles, tests, answers and results,
and calls the speech and LLM services.

Requirements: Go 1.22+

Run:

```
cd src/backend
go run ./cmd/server
```

The server starts on the port from `APP_PORT` (default 8080).
Check it: http://localhost:8080/health

Folders:

| Folder | What is inside |
| --- | --- |
| `cmd/server/` | `main.go`, the entry point |
| `config/` | Reads settings from environment variables |
| `handlers/` | HTTP handlers (API endpoints) |
| `models/` | Data structures (User, Test, Answer) |
| `services/` | Business logic, calls to speech and LLM services |

Tests:

```
go test ./...                    # unit tests next to the code
cd ../../tests/backend && go test ./...    # API tests
```
