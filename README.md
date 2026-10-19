# [TEMPORARY NAME] AI: Intelligent Knowledge Control System

Diploma project (AITU). The system checks how well students learn a topic.
A student answers questions by voice, the speech service turns the answer into text,
and the LLM service evaluates the answer. Teachers, students, parents and organization
admins each have their own cabinet.

## Repository structure

```
.
├── src/                     Source code, one folder per component
│   ├── frontend/            React web app (cabinets for all roles)
│   ├── backend/             Main REST API (FastAPI)
│   ├── speech_service/      Speech-to-text service
│   └── llm_service/         Answer evaluation with an LLM
├── tests/                   Tests, same structure as src/
├── docs/                    Project documents
│   ├── proposal/            Project proposal
│   ├── literature-review/   Literature review and references
│   ├── comparisons/         Technology comparisons
│   ├── requirements/        Functional and non-functional requirements
│   └── architecture/        Architecture Decision Records (ADR)
├── diagrams/
│   ├── src/                 Editable diagram sources (.drawio, .puml, .mmd)
│   └── exports/             Exported images (.png, .svg, .pdf)
├── config/                  Config examples with placeholder values
├── .env.example             Environment variables example (copy to .env)
└── .gitignore
```

## Getting started

1. Copy the example config files and fill in your own values:

    ```
    cp .env.example .env
    cp src/frontend/.env.example src/frontend/.env
    cp config/app.example.yaml config/app.yaml
    ```

2. Backend and services (Python 3.11+):

    ```
    python -m venv .venv
    source .venv/bin/activate          # Windows: .venv\Scripts\activate
    pip install -r src/backend/requirements.txt -r requirements-dev.txt
    uvicorn app.main:app --reload --app-dir src/backend
    ```

3. Frontend (Node.js 20+):

    ```
    cd src/frontend
    npm install
    npm run dev
    ```

4. Tests:

    ```
    pytest                          # backend and service tests
    cd src/frontend && npm test     # frontend tests
    ```

## Security and personal data

- Never commit passwords, API keys, tokens or real `.env` files.
- Only `*.example` files are committed. They contain placeholder values.
- Student voice recordings, answers and any real user data are personal data.
  Keep them only in `data/` or `uploads/`, which are ignored by Git.
- For tests, use generated or fake data only.
- If a secret was committed by mistake, change (rotate) the secret first,
  then remove it from the Git history.

## Team

| Role | Member |
| --- | --- |
| Frontend (React) | Erma |
| Backend | |
| ML / Speech and LLM | |
