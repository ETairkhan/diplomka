# DATERA EDU

**Intelligent Knowledge Control System** - a diploma project at Astana IT University.

Development of an intelligent system for monitoring student knowledge acquisition using speech recognition technologies and large language models for analyzing teacher-student dialogue

## Problem, users and aim

Teachers need a record of each student’s difficulties, parents need a clear picture of progress, and students need to know what to practise next. Five interviews with three parents, one teacher and one student informed the requirements. Assumptions that were not checked in the interviews are identified in the [Evidence of Relevance](docs/evidence-of-relevance.pdf).

**Target users:** tutors, language schools, online schools, learning centres, students and parents.

**Aim:** build and evaluate a system that checks students’ answers against course materials and tracks understanding by topic.

**Expected outcomes:** less time spent reviewing lessons, clearer progress reports, a personal list of topics to repeat, and a history of assessments. These outcomes will be evaluated in the pilot.

## Team

| Member | Role and responsibilities |
|---|---|
| David Khamitskiy | Project manager, ML/AI: requirements, priorities, speech processing, LLM analysis, evaluation and fine-tuning |
| Tairkhan Yermek | Backend: Go API, database, queue, file storage, authorisation and ML integration |
| Yermakhan Khamitov | Frontend: Figma prototype, web interface, reports, knowledge map and recording player |

**Supervisor:** Khaimuldin Nursultan Gazizovich

## Scope and current status

**First pre-defense - 24 October 2026:** the submission focuses on analysis, requirements, design and planning. The documents and diagrams below are available. Starter code exists; the complete application and ML pipeline are still under development.

**MVP - early March 2027:** materials and confirmed topics, lesson upload, speech recognition and speaker separation, analysis, three reports, a knowledge map, teacher corrections, consent and role-based access. It covers one-to-one lessons in English, Russian and mixed English–Russian speech.

**Stage 2 - March–April 2027:** tests on weak topics, weekly summaries, notifications and evaluation of a fine-tuned open language model. A trial fine-tuning experiment on open data is planned for late winter 2027.

**Outside the MVP:** Kazakh, group lessons, automatic student identification by voice and video-call integrations.

**Next steps:** address supervisor feedback, confirm GPU access and consented recordings, implement the core flow, and run the verification plan. The pilot is planned for March–April 2027 and the thesis write-up for April–May 2027.

## Documentation

The table follows the 11 pre-defense evaluation components. Documents contain the detailed evidence, requirements and decisions.

| # | Component | Material |
|---|---|---|
| 1 | Project proposal | [Project Proposal](docs/project-proposal.pdf) - problem, users, aim, objectives, outcomes and scope |
| 2 | Evidence of relevance | [Evidence of Relevance](docs/evidence-of-relevance.pdf) - five interviews, findings, assumptions and their effect on requirements |
| 3 | Literature review | [Literature Review](docs/literature-review.pdf) - structured analysis of 19 scientific articles and 10 technical sources, approaches and limitations |
| 4 | Existing system comparison | [Existing Systems Comparison](docs/existing-systems-comparison.pdf) - five systems compared using nine criteria |
| 5 | Technology comparison | [Technology Comparison](docs/technology-comparison.pdf) - 13 technical decisions, alternatives and requirement-based justification |
| 6 | Requirements specification | [Requirements Specification](docs/requirements-specification.pdf) - functional and non-functional requirements, priorities and acceptance criteria |
| 7 | Architecture and diagrams | [Architecture](docs/architecture.md) and the diagrams below - components, data and processing scenarios |
| 8 | UX / prototype | [Figma prototype](https://www.figma.com/design/oVOPB0JhPKVFBVWMuBbSlG/DATERA-EDU---UI?node-id=28-6) - user screens and key scenarios |
| 9 | Verification and evaluation | [Verification Plan](docs/verification-plan.pdf) - tests, metrics, measurement conditions, targets and baselines |
| 10 | Project management and risks | [Project Management and Risks](docs/project-management-and-risks.pdf) and [YouTrack](https://yakarta.youtrack.cloud/agiles/177-28/current) - responsibilities, milestones, tasks, risks and dependencies |
| 11 | Supervisor feedback | Review comments, agreed actions and resulting revisions still need to be linked here; no dedicated feedback record was found in the repository |

The **Requirements Traceability** document links requirements to components and checks. It is available in the [Requirements Traceability](docs/requirements-traceability.pdf)

## Diagrams

The context, use-case and component diagrams are required for the first pre-defense. BPMN and ER diagrams provide additional process and database detail.

| Diagram | View | Editable source |
|---|---|---|
| System context | [PNG](diagrams/context-diagram.png) | [draw.io](diagrams/context-diagram.drawio) |
| Use cases | [PNG](diagrams/use-case-diagram.png) | [draw.io](diagrams/use-case-diagram.drawio) |
| Components | [PNG](diagrams/component-diagram.png) | [draw.io](diagrams/component-diagram.drawio) |
| Lesson-analysis process (BPMN) | [PNG](diagrams/bpmn-lesson-analysis.png) | [draw.io](diagrams/bpmn-lesson-analysis.drawio) |
| Database structure (ER) | [JPG](diagrams/er-diagram.jpg) | [draw.io](diagrams/er-diagram.drawio) |

## Selected technologies

| Part | Technology |
|---|---|
| Frontend | React, TypeScript, Vite; planned UI libraries: shadcn/ui, TanStack Query, Recharts, wavesurfer.js |
| Backend | Go, REST, OpenAPI |
| Speech and ML | Python, PyTorch, ffmpeg, faster-whisper large-v3, pyannote.audio |
| LLM | Cloud model through an adapter with anonymised text; QLoRA fine-tuning and possible local deployment in stage 2 |
| Data and messaging | PostgreSQL 16 + pgvector, RabbitMQ, Redis, MinIO |
| Deployment | Docker Compose and Nginx |

These are design choices; full integration is planned. Alternatives and selection criteria are documented in the [Technology Comparison](docs/technology-comparison.pdf).

## Project links and submission

- [GitHub repository](https://github.com/ETairkhan/diplomka)
- [YouTrack tasks](https://yakarta.youtrack.cloud/agiles/177-28/current)
- [Figma prototype](https://www.figma.com/design/oVOPB0JhPKVFBVWMuBbSlG/DATERA-EDU---UI?node-id=28-6)
- [All working documents on Google Drive](https://drive.google.com/drive/folders/1lOMblVEHawU8rGmMv2vU9GCae2ZH8WaZ)

The submission materials are in `docs/` and `diagrams/`. Source code, tests and configuration remain in `src/`, `tests/` and `config/` as development continues.

Each meaningful change should be linked to a YouTrack task with an owner, priority, deadline and acceptance criteria. Changes go through a branch and a pull request reviewed by another team member. Each student uses an identifiable personal account.

Before submission, confirm access for the supervisor and committee, record supervisor feedback and revisions, and prepare examples of individual contributions and task-to-commit/PR links. Tag the reviewed submission `pre-defense-1` and record completed work, limitations and outstanding tasks. These checks are not confirmed by this README alone.

## Run the available starter code

The full application is not ready. These commands run and check the existing foundation. Requirements: Go 1.22+, Node.js 20+ and Python 3.11+.

Clone and prepare local configuration:

```bash
git clone https://github.com/ETairkhan/diplomka.git
cd diplomka
cp .env.example .env
cp src/frontend/.env.example src/frontend/.env
```

Fill in local values. Keep credentials and real recordings out of Git; use example configuration and synthetic test data.

Backend, from the repository root (the Go starter does not load `.env` automatically):

```bash
set -a
source .env
set +a
cd src/backend
go run ./cmd/server
```

Check `http://localhost:8080/health`. The expected response is `{"status":"ok"}`.

Frontend, in another terminal from the repository root:

```bash
cd src/frontend
npm ci
npm run dev
```

Open `http://localhost:5173`.

## Tests

Run each block from the repository root.

```bash
# Go unit and handler tests
go test ./src/backend/... ./tests/backend/...
```

```bash
# Frontend tests and build
cd src/frontend
npm ci
npm test
npm run build
```

```bash
# Current ML helper tests
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r src/ml_service/requirements.txt -r requirements-dev.txt
python -m pytest tests/ml_service
```

