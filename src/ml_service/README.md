# ML service (Python)

Worker that takes lesson-processing jobs from the RabbitMQ queue and runs the pipeline
from the technical specification (section 5.2):

| Stage | Module | Tool |
| --- | --- | --- |
| 1. Preparation | `ml/preprocessing.py` | ffmpeg: mono, 16 kHz, loudness normalization |
| 2. Denoising | `ml/denoise.py` | DeepFilterNet / Demucs / RNNoise (chosen by comparison) |
| 3. Speech recognition | `ml/asr.py` | faster-whisper large-v3 |
| 4. Diarization | `ml/diarization.py` | pyannote.audio |
| 5. LLM analysis | `ml/llm/` | LLM through an adapter, anonymized transcript |

Status: module structure and helper functions only. The models are not connected yet.

Audio of lessons is personal data (including minors). It is never stored in the repository.
