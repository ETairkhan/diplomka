# Intelligent Knowledge Control System

Working name: **"... AI"** (the final name will be chosen by the team).

A web system that automatically builds knowledge reports from a recorded lesson.
The teacher uploads a lesson recording. The system cleans the audio, turns speech into text,
finds out who is speaking (teacher or student), and an LLM analyzes the dialogue.
As a result, the teacher, the student and the parent each get a report: which topics
the student understands and which topics need more work. The student also gets a test
on the weak topics.

Diploma project (graduation thesis), Astana IT University. Full requirements are in the
[technical specification](docs/requirements/technical-specification.pdf) (in Russian).

## Problem statement

Today knowledge control after a lesson is manual:

- The teacher has to remember what was covered in earlier lessons. When the teacher changes,
  this history is lost.
- Parents learn about problems only from test grades, which is too late.
- Re-watching a lesson recording takes as long as the lesson itself, so in practice nobody does it.

As a result, gaps in a student's knowledge are found late, and the teacher spends a lot of
time preparing for the next lesson.

## Target users

Target customers: online schools and learning centers, private tutors, specialized schools.
The system works with any subject that is taught through spoken explanation.

| Role | Cabinet | Main actions |
| --- | --- | --- |
| Organization admin | Organization | Manages teachers, students, groups and the question bank; sees analytics for all students |
| Teacher | Organization | Uploads lesson recordings, checks speaker labels, reads reports, assigns tests |
| Student | Student | Reads reports, sees the knowledge map and lesson recordings, takes tests |
| Parent | Parent | Gives consent for recording processing, reads reports and weekly summaries |
| System admin | Service | Manages organizations, models and prompts, monitors the processing queue |

A private tutor registers as an organization of one person.

## Expected outcomes

1. Less teacher time spent on lesson analysis and preparation for the next lesson.
2. A clear picture of the child's progress for parents, without special terms.
3. A personal list of topics to repeat and tests that close the student's own gaps.
4. Objective progress data for the organization that is kept when a teacher changes.

Target quality metrics (from the technical specification):

| Metric | Target |
| --- | --- |
| Report time for a 60-minute lesson | not more than 30 minutes |
| Speech recognition error (WER) | not more than 20 % |
| Diarization error (DER) | not more than 20 % |
| Topic status agreement with the teacher's assessment | at least 70 % of topics |
| LLM answers that match the JSON schema | at least 95 % |

## Team

| Member | Role | Responsibilities |
| --- | --- | --- |
| David | Product manager, ML/AI | Requirements, priorities, acceptance; ML pipeline (audio cleaning, Whisper, diarization); LLM prompts and quality evaluation |
| Tairkhan | Backend developer | Go API, database, task queue, file storage, authorization, integration with the ML service |
| Yermakhan | Frontend developer | Web interface of the three cabinets, progress visualization, recording player with time codes, tests for students; Figma mockups |

Supervisor: **<add supervisor's full name and position>**

## Project scope

### In scope (MVP, required for the defense)

- Registration, login and role-based access (organization, teacher, student, parent)
- Electronic consent for recording processing (from the parent if the student is under 18)
- Study structure: subjects, groups, students and teachers
- Upload of lesson recordings (audio or video) with processing status
- Audio preprocessing and denoising
- Speech recognition with time codes and speaker diarization
- LLM analysis of the lesson: topics, scores, summary, recommendations
- Knowledge index (0-100 %) and knowledge map for each student
- Reports after each lesson and weekly summaries, a separate version for each role
- Question bank and tests on weak topics
- In-app notifications and system administration
- Lessons in Russian; individual lessons fully, group lessons in a simple form
  (the teacher matches voices to students manually)

### Out of scope (future development)

- Kazakh and mixed Russian-Kazakh speech
- Automatic recognition of students by voice in group lessons
- Login with Google and other external providers
- Lesson recording in the browser, Zoom / Google Meet integration
- Notifications by email, Telegram and push; PDF export; monthly summaries
- Open-answer questions checked by an LLM; LLM-generated questions
- ML forecast of test risk; teacher efficiency analytics

### Timeline

| Event | Date |
| --- | --- |
| Approval of the technical specification | November 2026 |
| Start of development | early November 2026 |
| Pre-defense 1 | October 24, 2026 |
| MVP ready | end of February - early March 2027 |
| Testing, metrics, thesis writing | March - May 2027 |
| Defense | early June 2027 |

## Current development status

Stage 1 of 9: **preparation** (as of October 2026).

| Area | Status |
| --- | --- |
| Technical specification | Draft written, approval planned for November 2026 |
| Repository, structure, config examples | Done |
| Backend (Go) | Project skeleton: server, config from environment, CORS, `GET /health`, unit and API tests |
| Frontend (React + TypeScript) | Project skeleton: routing, login page, API client, test setup. Figma mockups of the three cabinets in progress |
| ML service (Python) | Module structure for the pipeline; audio preparation command, speaker merge and anonymization helpers with tests. Models are not connected yet |
| Database, queue, file storage, Docker Compose | Not started (next stage) |
| Model comparison (denoising, ASR, diarization, LLM) | Planned; templates are in `docs/comparisons/` |

Next steps: collect 15+ test lesson recordings with consent, set up the GPU server and Docker
environment, compare ML models, implement registration, roles and file upload (FR-1 - FR-4).

## Technologies

| Part | Technology |
| --- | --- |
| Frontend | React, TypeScript, Vite; charts: Recharts or ECharts; player: wavesurfer.js |
| Backend API | Go (Gin or chi), REST, OpenAPI |
| Database | PostgreSQL 16 + pgvector |
| Task queue | RabbitMQ |
| Cache | Redis |
| File storage | MinIO (S3-compatible), audio is deleted after 30 days |
| ML service | Python 3.11, PyTorch (CUDA), ffmpeg |
| Denoising | DeepFilterNet / Demucs / RNNoise (chosen by comparison) |
| Speech recognition | faster-whisper, large-v3 |
| Diarization | pyannote.audio |
| LLM | Through an adapter; cloud LLM with anonymized text for the MVP, local model as an alternative |
| Deployment | Docker, Docker Compose, Nginx (HTTPS) |

Architecture: [component diagram](diagrams/src/components.mmd), [context diagram](diagrams/src/context.puml).

## Links

| Resource | Link |
| --- | --- |
| YouTrack project (tasks) | <add YouTrack project link> |
| Figma mockups | <add Figma link> |
| Documentation index | [docs/README.md](docs/README.md) |
| Technical specification | [docs/requirements/technical-specification.pdf](docs/requirements/technical-specification.pdf) |
| Requirements | [docs/requirements/](docs/requirements/) |
| Technology comparisons | [docs/comparisons/](docs/comparisons/) |
| Architecture decisions (ADR) | [docs/architecture/](docs/architecture/) |
| Diagrams | [diagrams/](diagrams/) |

## Repository structure

```
.
├── src/
│   ├── frontend/        React + TypeScript web client
│   ├── backend/         Go REST API
│   └── ml_service/      Python ML pipeline (denoising, ASR, diarization, LLM)
├── tests/               Tests: backend/, ml_service/, frontend/, e2e/, fixtures/
├── docs/                Proposal, literature review, comparisons, requirements, ADR
├── diagrams/            src/ (editable sources) and exports/ (images)
├── config/              Config examples with placeholder values
├── .env.example         Environment variables example
├── go.work              Go workspace (backend + backend tests)
└── requirements-dev.txt Python test tools
```

## Setup

Requirements: Go 1.22+, Node.js 20+, Python 3.11+.

```
git clone <repository-url>
cd knowledge-control-system
cp .env.example .env                              # then fill in your own values
cp src/frontend/.env.example src/frontend/.env
```

## Run

Backend API (http://localhost:8080):

```
cd src/backend
go run ./cmd/server
```

Check: open http://localhost:8080/health, the answer is `{"status":"ok"}`.

Frontend (http://localhost:5173):

```
cd src/frontend
npm install
npm run dev
```

ML service: the models are not connected yet, so only the tests can be run (see below).
Running all services with one command (Docker Compose) will be added in the next stage.

## Tests

```
# Backend unit tests
cd src/backend && go test ./...

# Backend API tests
cd tests/backend && go test ./...

# ML service tests (from the repository root)
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\\Scripts\\activate
pip install -r src/ml_service/requirements.txt -r requirements-dev.txt
pytest

# Frontend tests
cd src/frontend && npm test
```

## Security and personal data

The system processes voice recordings, including recordings of minors, so it follows the
Law of the Republic of Kazakhstan "On Personal Data and Their Protection".

- Passwords, API keys, tokens and real `.env` files are never committed.
  Only `*.example` files with placeholder values are in the repository.
- Lesson recordings and any real user data are never stored in the repository
  (`data/`, `uploads/` and audio files are ignored by Git). Tests use fake data only.
- Only an anonymized transcript (without names) is sent to an external LLM.
- If a secret is committed by mistake: change (rotate) it first, then remove it from the Git history.
