# DATERA EDU — Architecture (draft)

Status: draft for pre-defense 1 (24 October 2026). Based on the technical specification (TZ DATERA). Codes FR-x refer to functional requirements (ФТ), NFR-x to non-functional requirements (НФТ).

Related diagrams in `diagrams/`:

- `system-context-diagram` — the system as a black box, its users and external systems.
- `component-diagram` — the inside of that box: containers, their components, data stores and connections.

Both diagrams use the same colours: black is MVP (early March 2027), purple is stage 2 (March–April 2027).

## 1. Overview

DATERA EDU takes a recording of an individual lesson and the teacher's materials, checks how the student answered on each topic, and builds reports for the teacher, the student and the parent, plus a knowledge map.

The system has three parts (TZ 5.1):

1. **Web client** (React) — three cabinets and admin pages in the browser.
2. **Backend API** (Go) — accounts, rights, learning structure, files, index, reports, scheduler.
3. **ML service** (Python, GPU) — audio cleaning, speech recognition, diarization, all LLM calls.

The API and the ML service do not call each other directly. They exchange tasks and results through RabbitMQ. This means an upload does not wait for the analysis, and a failure of the ML service or the LLM does not stop the cabinets (TZ 5.3, 5.4).

All services run on one server in Kazakhstan with Docker Compose (NFR-4.1, NFR-7.1). The only data that leaves the server in the MVP is anonymised text sent to the cloud LLM (NFR-4.2).

## 2. Components

### 2.1 Web client

| Component | Responsibility | Requirements |
| --- | --- | --- |
| Organisation cabinet | Admin screens (accounts, subjects, links) and teacher screens (materials and topics, upload, status, reports, transcript, knowledge map, student list) | FR-1.2, FR-3, FR-4, FR-6.7, FR-8.7, FR-11.1, FR-11.5 |
| Student cabinet | Lesson feed with reports and player, knowledge map, "what to review" | FR-12.1–12.2 |
| Parent cabinet | Children switch, lesson reports, knowledge map | FR-13.1–13.3 |
| System admin pages | Queue and errors, LLM model and prompt versions | FR-15.2–15.3 |

Technology: React + TypeScript, Vite, shadcn/ui, TanStack Query, Recharts, wavesurfer.js (table 9). Interface language is Russian; texts are in translation files (NFR-6.3).

### 2.2 Nginx

Terminates HTTPS (NFR-3.1). Routes `/api` to the Backend API and `/media` to MinIO. Audio is played only by a signed URL that lives 15 minutes (NFR-3.5).

### 2.3 Backend API (Go, Gin or chi, REST + OpenAPI)

| Component | Responsibility | Requirements |
| --- | --- | --- |
| Auth & access | Registration, invitation links, JWT (access 15 min + refresh), roles, server-side checks on every request, login limit | FR-1, NFR-3.2–3.4, NFR-3.7 |
| Consent | Consent for processing and separate consent for training; blocks upload without consent | FR-2.1–2.4, NFR-4.4 |
| Learning structure | Subjects, student–teacher–subject links, materials, topic list and its confirmation | FR-3.1–3.7 |
| Lessons & upload | Upload of recordings, lesson metadata and language, retry after error | FR-4.1–4.6 |
| Pipeline orchestrator | Publishes tasks, reads events, keeps the stage status shown to the user | FR-4.5, NFR-2.1–2.3 |
| Index & knowledge map | Index and colour status by formula, knowledge map, history, teacher confirmation or change | FR-8.1–8.2, FR-8.6–8.7 |
| Reports & cabinet views | Stores report texts, puts real names back, gives each role its own view | FR-7.6, FR-9, FR-11–FR-13 |
| Training data | Saves every teacher confirmation or change as a row in `training_examples` (anonymised, only with consent); in stage 2 exports the set and sends it to the training GPU server | FR-16.1, FR-16.3, NFR-4.5 |
| Scheduler | Deletes audio 30 days after upload | FR-4.7, NFR-4.3 |
| Admin & monitoring | Queue and errors by stage, model and prompt versions; access log in stage 2 | FR-15.2–15.4 |
| Tests & question bank *(stage 2)* | Question bank, test assembly, auto-check, index update | FR-10 |
| Notifications & digests *(stage 2)* | In-app notifications and weekly digest in the cabinet; email is sent only for password reset (email notifications are future, FR-14.2) | FR-1.5, FR-9.5, FR-14.1 |

Business numbers (index, statuses, risk) are calculated only here, by code. The LLM never changes them (TZ 5.2, 5.3).

### 2.4 ML service (Python 3.11, PyTorch CUDA)

| Component | Responsibility | Requirements |
| --- | --- | --- |
| Task worker | Takes tasks from `ml.tasks`, runs stages, saves a checkpoint after each stage, retries a stage up to 3 times | NFR-2.2–2.3, NFR-7.6 |
| Stage 0 · Preparation | ffmpeg: audio from video, mono 16 kHz, loudness | FR-4.4, FR-5.1 |
| Stage 1 · Denoise + VAD | Noise reduction (DeepFilterNet / Demucs / RNNoise, chosen by WER) and speech detection; can be switched off per recording | FR-5.2–5.5 |
| Stage 2 · Speech recognition | faster-whisper large-v3, English, Russian and mixed speech, word timecodes | FR-6.1 |
| Stage 3 · Diarization | pyannote.audio, merge with text, find the teacher, pauses and repeats | FR-6.2–6.6 |
| Material topics | Text from PDF, DOCX, PPTX, TXT, MD; topic list via LLM; vectors for topic matching | FR-3.5, FR-7.1 |
| Anonymiser | Replaces names with labels ("Teacher", "Student 1") before any LLM call | FR-7.6 |
| Stage 4 · LLM analysis | Finds where confirmed topics were discussed, checks answers against the material, status with reasons and timecodes, "outside material" fragments, summary | FR-7.1–7.5, FR-7.8 |
| Stage 5 · Report writer | Report texts for teacher, student and parent, in each reader's language | FR-9.1–9.2 |
| LLM adapter | One interface for all LLM calls; provider and model set in config; JSON schema check and up to 3 repeats | FR-7.5, FR-7.7, FR-15.3 |

### 2.5 Data stores and infrastructure

| Store | What it keeps | Requirements |
| --- | --- | --- |
| PostgreSQL 16 + pgvector | All business data, including `training_examples`; vectors of topics and material fragments | Table 9, FR-7.1, FR-16.1 |
| MinIO (S3) | Original and cleaned audio (encrypted), teacher materials, stage checkpoints | FR-3.7, FR-4.7, FR-5.5, NFR-3.6 |
| RabbitMQ | Queues `ml.tasks` and `ml.events`; durable, persistent messages, manual ack | NFR-2.1 |
| Redis | Sessions and login attempt counter | NFR-3.7 |
| Local LLM server *(stage 2)* | vLLM with the fine-tuned Qwen / Llama 7–9B model | FR-16.4–16.6 |

### 2.6 External systems

The same as in the context diagram:

- **Cloud LLM API** (MVP): gets only anonymised transcript and material text, returns JSON.
- **Email service (SMTP)** (stage 2): password reset emails only (FR-1.5).
- **Training GPU server** (stage 2): university server or rented GPU in Kazakhstan; gets the anonymised training set exported by the Backend API, returns the fine-tuned model; data is deleted after training (NFR-4.5).

## 3. Main data

The full schema (32 tables) is in `docs/schema.sql`, the ER diagram in `diagrams/er-diagram.*`, and the description in `docs/database.md`. The main groups are:

| Group | Tables |
| --- | --- |
| Accounts & access | `organizations`, `users`, `user_roles`, `invitations`, `students`, `parent_students`, `consents` |
| Learning structure | `subjects`, `enrollments`, `materials`, `material_chunks`, `topics` |
| Lessons & processing | `lessons`, `audio_files`, `speakers`, `transcript_segments`, `processing_events` |
| Analysis & knowledge map | `lesson_analyses`, `topic_assessments`, `off_material_fragments`, `knowledge_map`, `index_history` |
| Reports, prompts & training | `reports`, `prompt_versions`, `training_examples` |
| Stage 2 | `questions`, `tests`, `test_questions`, `test_attempts`, `attempt_answers`, `notifications`, `access_logs` |

Retention: audio 30 days; transcripts, reports and the knowledge map until the student account is deleted or consent is withdrawn (NFR-4.3).

## 4. Queue contract

| Message | Direction | Content |
| --- | --- | --- |
| `extract_topics` | API → ML | material id, MinIO path, subject |
| `process_lesson` | API → ML | lesson id, audio path, language, confirmed topics, participant names for anonymisation, denoise on/off |
| `write_reports` | API → ML | lesson id, analysis result, index and statuses, reader languages |
| `status` | ML → API | lesson id, stage, state (started / done / error, reason) |
| `result` | ML → API | topics, transcript, analysis JSON or report texts, model and prompt version |

Each message carries the lesson id, which is also written to the structured logs of all services (NFR-7.5).

## 5. Key scenarios

The scenarios follow the acceptance scenarios in TZ 10.3.

**S1. Materials and topics**

1. The teacher uploads a PDF.
2. The API stores it in MinIO and publishes `extract_topics`.
3. The ML service extracts the text, the LLM suggests topics, and vectors are calculated.
4. The API saves the topics as suggested.
5. The teacher confirms, renames, merges or deletes them (FR-3.4–3.6).

**S2. Lesson recording to reports (main MVP scenario)**

1. The teacher uploads a video. The API checks consent (FR-2.1), stores the file in MinIO, creates the lesson and publishes `process_lesson`.
2. The ML service runs stages 0–3 and publishes a `status` event after each one. The user sees the status change (FR-4.5).
3. Stage 4 sends the anonymised transcript and the relevant material fragments (found by pgvector) through the adapter to the cloud LLM. The JSON is checked and repeated up to 3 times (FR-7.5).
4. The API saves the assessments and calculates the index, colours and knowledge map (FR-8.1). Then it publishes `write_reports`.
5. Stage 5 writes the report texts. The API puts the real names back and saves each report with the model and prompt version (FR-7.6, FR-15.3).
6. Target: a 60-minute lesson is ready in 30 minutes or less (NFR-1.1).

**S3. Viewing a report**

1. Each role opens its own version of the report. The API checks rights on every request (NFR-3.4).
2. A click on a timecode gets a signed URL, and the player opens that moment (FR-9.4).
3. After the audio is deleted, the transcript fragment is shown instead.

**S4. Teacher correction**

1. The teacher fixes the speaker labels, and the analysis runs again from stage 4 (FR-6.4).
2. The teacher confirms or changes a topic status. The index and the map are recalculated, and the change goes to the history (FR-8.7).
3. A training example is saved if the training consent exists (FR-16.1).

**S5. Retention and consent withdrawal**

1. The scheduler deletes audio after 30 days (FR-4.7).
2. On a withdrawal request, the system admin deletes the student's recordings, transcripts and reports within 3 working days (FR-2.4).

**S6. Model switch (stage 2)**

1. The Backend API exports `training_examples` (anonymised, only lessons with training consent) and sends the set to the training GPU server.
2. The fine-tuned model is deployed to vLLM.
3. The system admin switches the adapter config. New lessons are then analysed by this model, and the report shows the model version (FR-16.6, TZ 10.3).

## 6. Main decisions

| Decision | Reason | Source |
| --- | --- | --- |
| Go API + separate Python ML service | The backend developer works in Go; speech and ML models are mainly in the Python ecosystem | TZ 5.3 |
| Asynchronous processing through RabbitMQ | Upload does not wait for analysis; tasks survive restarts; ML workers scale by adding instances | TZ 5.3, NFR-2.1, NFR-7.6 |
| One multilingual ASR model (Whisper large-v3) | Handles English, Russian and mixed speech without switching models | TZ 5.3, FR-6.1 |
| Topics come from the teacher's materials | No fixed curriculum needed; the "correct answer" is defined by the material, not by the model's general knowledge | TZ 5.3, FR-3.5–3.6 |
| LLM adapter + anonymisation | The model can be changed by config; only text without names leaves the server | FR-7.6–7.7, NFR-4.2 |
| Rules over LLM | Index, statuses and risk are calculated by code, so results are reproducible | TZ 5.3 |
| Checkpoint after each stage | Processing continues from the last finished stage after a failure | NFR-2.2 |

The alternatives for these choices are compared in the technology comparison document.

## 7. Non-functional requirements in the architecture

| NFR | How the architecture supports it |
| --- | --- |
| NFR-1.1–1.2 Report in 30 min, 10 lessons a day | GPU for stages 1–3; lessons processed one by one from the queue |
| NFR-1.3 API under 500 ms | Long work is in the queue; the API only reads and writes the database |
| NFR-2.1–2.3 Reliability | Durable queue, manual ack, checkpoints, 3 retries per stage |
| NFR-3 Security | Nginx HTTPS, JWT, server-side role checks, signed URLs, encrypted audio, Redis login limit |
| NFR-4 Personal data | One server in Kazakhstan, anonymiser before the cloud LLM, 30-day audio deletion, separate training consent |
| NFR-7 Maintainability | Docker Compose, OpenAPI, stateless API, one lesson id in all logs |

## 8. Open questions for this draft

1. **Embedding model.** Topic and material vectors are needed for FR-7.1, but table 9 does not name the model. Proposal: a multilingual sentence-embedding model in the ML service. To be added to the technology comparison.
2. **Materials storage.** Table 9 lists MinIO only for audio. This draft also keeps teacher materials there (FR-3.7). Confirm, or store them in PostgreSQL.
3. **Text extraction from materials.** The library for PDF, DOCX and PPTX is not chosen yet.
4. **Report writing on reprocessing.** When the teacher changes a status (S4), it is not decided whether the report texts are written again or only the numbers are updated.
