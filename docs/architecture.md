# DATERA EDU: Architecture

Status: draft. It follows the technical specification (Requirements specification). FR-x codes are functional requirements, NFR-x codes are non-functional ones, as in the technical specification.

Diagrams (folder `diagrams/`, editable `.drawio` files and `.png` copies):

- `context-diagram` \- the system as one box: who uses it and which outside services it talks to.  
- `use-case-diagram` \- what each user can do in the MVP.  
- `component-diagram` \- what is inside the box: services, their parts, data stores and links.  
- `bpmn-lesson-analysis` \- the path of one lesson from consent to reports, by role.

Stage 2 parts are marked separately on the diagrams. Everything else is the MVP, planned for early March 2027\.

## 1\. Overview

The teacher uploads study materials and then the recording of a one-to-one lesson. DATERA EDU checks how the student answered on each topic and builds three reports (teacher, student, parent) and a knowledge map.

The system has three parts (technical specification, section 5.1):

1. **Web client** (React). Three cabinets and a few admin pages in the browser.  
2. **Backend API** (Go). Accounts, rights, subjects and materials, files, the index, reports and a scheduler.  
3. **ML service** (Python, GPU). Audio cleaning, speech recognition, speaker separation and every call to the language model.

The API and the ML service never call each other directly. They pass tasks and results through RabbitMQ. Because of this, an upload does not wait for the analysis, and the cabinets keep working when the ML service or the language model is down (technical specification, sections 5.3 and 5.4).

All services run on one server in Kazakhstan under Docker Compose (NFR-4.1, NFR-7.1). In the MVP the only data that leaves the server is anonymised text sent to the cloud language model (NFR-4.2).

## 2\. Components

### 2.1 Web client

| Component | What it does | Requirements |
| :---- | :---- | :---- |
| Organisation cabinet | Admin screens (accounts, subjects, links) and teacher screens (materials and topics, upload, status, reports, transcript, knowledge map, student list) | FR-1.2, FR-3, FR-4, FR-6.7, FR-8.7, FR-11.1, FR-11.5 |
| Student cabinet | Lesson feed with reports and player, knowledge map, "what to repeat" | FR-12.1 \- FR-12.2 |
| Parent cabinet | Child switch, lesson reports, knowledge map | FR-13.1 \- FR-13.3 |
| System admin pages | Queue and errors, model and prompt versions | FR-15.2 \- FR-15.3 |

Technologies: React with TypeScript, Vite, shadcn/ui, TanStack Query, Recharts, wavesurfer.js (Table 9 of the technical specification). The interface is in Russian, and all texts sit in translation files (NFR-6.3).

### 2.2 Nginx

Accepts HTTPS (NFR-3.1) and sends `/api` to the Backend API and `/media` to MinIO. Audio plays only through a signed link that works for 15 minutes (NFR-3.5).

### 2.3 Backend API (Go, Gin or chi, REST with OpenAPI)

| Component | What it does | Requirements |
| :---- | :---- | :---- |
| Auth & access | Registration, invitation links, JWT (access token 15 minutes plus refresh token), roles, rights checked on the server for every request, login attempt limit | FR-1, NFR-3.2 \- NFR-3.4, NFR-3.7 |
| Consent | Consent to processing and a separate consent to training; blocks upload when there is no consent | FR-2.1 \- FR-2.4, NFR-4.4 |
| Learning structure | Subjects, links between student, teacher and subject, materials, the topic list and its confirmation | FR-3.1 \- FR-3.7 |
| Lessons & upload | Recording upload, lesson data and language, restart after an error | FR-4.1 \- FR-4.6 |
| Pipeline orchestrator | Sends tasks to the queue, reads events, keeps the processing status the user sees | FR-4.5, NFR-2.1 \- NFR-2.3 |
| Index & knowledge map | Index and colour status by formula, knowledge map, history, teacher's confirmation or change | FR-8.1 \- FR-8.2, FR-8.6 \- FR-8.7 |
| Reports & cabinet views | Stores report texts, puts real names back, shows each role its own version | FR-7.6, FR-9, FR-11 \- FR-13 |
| Training data | Saves every confirmation or change by the teacher as a row in `training_examples` (anonymised, only with consent). In stage 2 it exports the set and sends it to the training GPU server | FR-16.1, FR-16.3, NFR-4.5 |
| Scheduler | Deletes audio 30 days after upload | FR-4.7, NFR-4.3 |
| Admin & monitoring | Queue and errors by stage, model and prompt versions; access log in stage 2 | FR-15.2 \- FR-15.4 |
| Tests & question bank *(stage 2\)* | Question bank, test assembly, automatic check, index update | FR-10 |
| Notifications & digests *(stage 2\)* | Notifications inside the cabinet and a weekly digest. E-mail is sent only for password reset (e-mail notifications are future work, FR-14.2) | FR-1.5, FR-9.5, FR-14.1 |

All numbers that matter (index, statuses, risk) are calculated here, by code. The language model never changes them (technical specification, sections 5.2 and 5.3).

### 2.4 ML service (Python 3.11, PyTorch with CUDA)

| Component | What it does | Requirements |
| :---- | :---- | :---- |
| Task worker | Takes tasks from `ml.tasks`, runs the stages, saves a checkpoint after each stage, repeats a failed stage up to 3 times | NFR-2.2 \- NFR-2.3, NFR-7.6 |
| Stage 0\. Preparation | ffmpeg: takes audio out of video, converts to mono 16 kHz, levels the volume | FR-4.4, FR-5.1 |
| Stage 1\. Denoise and VAD | Noise reduction (DeepFilterNet, Demucs or RNNoise, chosen by WER) and speech detection. Can be switched off for one recording | FR-5.2 \- FR-5.5 |
| Stage 2\. Speech recognition | faster-whisper large-v3 for English, Russian and mixed speech, with word time codes | FR-6.1 |
| Stage 3\. Speaker separation | pyannote.audio, joining with the text, finding the teacher, pauses and repeats | FR-6.2 \- FR-6.6 |
| Material topics | Text from PDF, DOCX, PPTX, TXT and MD; topic list through the language model; vectors for matching topics | FR-3.5, FR-7.1 |
| Anonymiser | Replaces names with labels ("Teacher", "Student 1") before any call to the language model | FR-7.6 |
| Stage 4\. Analysis | Finds where each confirmed topic was discussed, checks the answers against the materials, gives a status with reasons and time codes, marks fragments "outside the materials", writes a summary | FR-7.1 \- FR-7.5, FR-7.8 |
| Stage 5\. Report writer | Writes the texts for the teacher, the student and the parent, each in the reader's language | FR-9.1 \- FR-9.2 |
| LLM adapter | One interface for all calls to a language model. Provider and model are set in the config. Checks the JSON against the schema and repeats up to 3 times | FR-7.5, FR-7.7, FR-15.3 |

### 2.5 Data stores and infrastructure

| Store | What it keeps | Requirements |
| :---- | :---- | :---- |
| PostgreSQL 16 with pgvector | All business data, including `training_examples`; vectors of topics and material fragments | Table 9, FR-7.1, FR-16.1 |
| MinIO (S3) | Original and cleaned audio (encrypted), teachers' materials, stage checkpoints | FR-3.7, FR-4.7, FR-5.5, NFR-3.6 |
| RabbitMQ | Queues `ml.tasks` and `ml.events`; durable, persistent messages, manual acknowledgement | NFR-2.1 |
| Redis | Sessions and the counter of login attempts | NFR-3.7 |
| Local LLM server *(stage 2\)* | vLLM with the fine-tuned Qwen or Llama model (7-9 billion parameters) | FR-16.4 \- FR-16.6 |

MinIO keeps both audio and materials, as decided in the Technology Comparison (decision 4).

### 2.6 External systems

The same as on the context diagram:

- **Cloud LLM API** (MVP). Gets only anonymised transcript and material text and returns JSON.  
- **E-mail service, SMTP** (stage 2). Only password reset e-mails (FR-1.5).  
- **Training GPU server** (stage 2). A university server or a rented GPU in Kazakhstan. It gets the anonymised training set exported by the Backend API and returns the fine-tuned model. The data is deleted after training (NFR-4.5).

## 3\. Main data

The database structure is represented in the ER diagram available in diagrams/er-diagram.png.

The schema contains 32 tables grouped by their functional purpose. The SQL schema and detailed database description will be maintained in docs/schema.sql and docs/database.md as the implementation progresses.

The tables fall into these groups:

| Group | Tables |
| :---- | :---- |
| Accounts and access | `organizations`, `users`, `user_roles`, `invitations`, `students`, `parent_students`, `consents` |
| Learning structure | `subjects`, `enrollments`, `materials`, `material_chunks`, `topics` |
| Lessons and processing | `lessons`, `audio_files`, `speakers`, `transcript_segments`, `processing_events` |
| Analysis and knowledge map | `lesson_analyses`, `topic_assessments`, `off_material_fragments`, `knowledge_map`, `index_history` |
| Reports, prompts and training | `reports`, `prompt_versions`, `training_examples` |
| Stage 2 | `questions`, `tests`, `test_questions`, `test_attempts`, `attempt_answers`, `notifications`, `access_logs` |

Retention: audio is kept 30 days. Transcripts, reports and the knowledge map are kept until the student account is deleted or the consent is withdrawn (NFR-4.3).

## 4\. Queue messages

| Message | Direction | Content |
| :---- | :---- | :---- |
| `extract_topics` | API to ML | material id, MinIO path, subject |
| `process_lesson` | API to ML | lesson id, audio path, language, confirmed topics, participant names for anonymisation, denoise on or off |
| `write_reports` | API to ML | lesson id, analysis result, index and statuses, reader languages |
| `status` | ML to API | lesson id, stage, state (started, done or error with a reason) |
| `result` | ML to API | topics, transcript, analysis JSON or report texts, model and prompt version |

Every message carries the lesson id. The same id is written to the logs of all services (NFR-7.5).

## 5\. Main flows

These flows follow the acceptance scenarios in section 10.3 of the technical specification. The numbered scenarios S1 \- S12 with pass criteria are in the Verification Plan, so the flows here are named Flow 1 \- Flow 6 to avoid mixing them up.

**Flow 1\. Materials and topics**

1. The teacher uploads a PDF.  
2. The API saves it in MinIO and sends `extract_topics`.  
3. The ML service extracts the text, the language model suggests topics, and the vectors are calculated.  
4. The API saves the topics as suggested.  
5. The teacher confirms, renames, merges or deletes them (FR-3.4 \- FR-3.6).

**Flow 2\. From recording to reports (the main MVP flow)**

1. The teacher uploads a video. The API checks the consent (FR-2.1), saves the file in MinIO, creates the lesson and sends `process_lesson`.  
2. The ML service runs stages 0 \- 3 and sends a `status` event after each one. The user sees the status change (FR-4.5).  
3. Stage 4 sends the anonymised transcript and the matching parts of the materials (found with pgvector) to the cloud language model through the adapter. The JSON is checked and repeated up to 3 times if needed (FR-7.5).  
4. The API saves the assessments and calculates the index, colours and knowledge map (FR-8.1). Then it sends `write_reports`.  
5. Stage 5 writes the report texts. The API puts the real names back and saves each report with the model and prompt version (FR-7.6, FR-15.3).  
6. Target: a 60-minute lesson is ready in 30 minutes or less (NFR-1.1).

**Flow 3\. Reading a report**

1. Each role opens its own version of the report. The API checks the rights on every request (NFR-3.4).  
2. A click on a time code gets a signed link, and the player opens that moment (FR-9.4).  
3. After the audio is deleted, the transcript fragment opens instead.

**Flow 4\. Teacher's correction**

1. The teacher fixes the speaker labels, and the analysis runs again from stage 4 (FR-6.4).  
2. The teacher confirms or changes a topic status. The index and the map are recalculated, and the change goes to the history (FR-8.7).  
3. If there is a consent to training, a training example is saved (FR-16.1).

**Flow 5\. Deleting data**

1. The scheduler deletes audio after 30 days (FR-4.7).  
2. When a parent withdraws consent, the system admin deletes the student's recordings, transcripts and reports within 3 working days (FR-2.4).

**Flow 6\. Switching the model (stage 2\)**

1. The Backend API exports `training_examples` (anonymised, only lessons with training consent) and sends the set to the training GPU server.  
2. The fine-tuned model is deployed to vLLM.  
3. The system admin changes the adapter config. New lessons are then analysed by this model, and the report shows its version (FR-16.6, section 10.3 of the technical specification).

## 6\. Main decisions

| Decision | Reason | Source |
| :---- | :---- | :---- |
| Go API and a separate Python ML service | The backend developer works in Go, and speech and ML models live mostly in Python | Technical specification 5.3 |
| Processing through RabbitMQ | Upload does not wait for the analysis, tasks survive a restart, more ML workers can be added | Technical specification 5.3, NFR-2.1, NFR-7.6 |
| One multilingual recognition model (Whisper large-v3) | It handles English, Russian and mixed speech without switching models | Technical specification 5.3, FR-6.1 |
| Topics come from the teacher's materials | No fixed curriculum is needed, and the right answer is defined by the materials, not by what the model knows in general | Technical specification 5.3, FR-3.5 \- FR-3.6 |
| LLM adapter and anonymisation | The model can be changed in the config, and only text without names leaves the server | FR-7.6 \- FR-7.7, NFR-4.2 |
| Rules instead of the language model for numbers | Index, statuses and risk come from code, so results can be repeated | Technical specification 5.3 |
| Checkpoint after each stage | After a failure, processing goes on from the last finished stage | NFR-2.2 |

The alternatives for these choices are compared in the Technology Comparison.

## 7\. Non-functional requirements and the architecture

| Requirement | How the architecture meets it |
| :---- | :---- |
| NFR-1.1 \- NFR-1.2. Report in 30 minutes, 10 lessons a day | GPU for stages 1 \- 3; lessons are processed one after another from the queue |
| NFR-1.3. API under 500 ms | Long work goes to the queue; the API only reads and writes the database |
| NFR-2.1 \- NFR-2.3. Reliability | Durable queue, manual acknowledgement, checkpoints, 3 repeats per stage |
| NFR-3. Security | HTTPS in Nginx, JWT, rights checked on the server, signed links, encrypted audio, login limit in Redis |
| NFR-4. Personal data | One server in Kazakhstan, anonymiser before the cloud model, audio deleted after 30 days, separate consent to training |
| NFR-7. Maintainability | Docker Compose, OpenAPI, stateless API, one lesson id in all logs |

## 8\. Open questions

1. **Embedding model.** Vectors of topics and material fragments are needed for FR-7.1, but the technical specification does not name the model. Proposal: a multilingual sentence-embedding model inside the ML service. It should be added to the open questions of the Technology Comparison.  
2. **Reports after a correction.** When the teacher changes a status (Flow 4), it is not decided whether the report texts are written again or only the numbers are updated.