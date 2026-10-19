# Configuration

This folder has **examples only**. Real config files are ignored by Git.

| File | Purpose |
| --- | --- |
| `app.example.yaml` | Main settings for the backend and services |
| `logging.example.yaml` | Logging settings |

How to use:

```
cp config/app.example.yaml config/app.yaml
cp config/logging.example.yaml config/logging.yaml
```

Secrets (passwords, API keys) go only into `.env`, never into YAML files.
The YAML files read them from environment variables, for example `${DB_PASSWORD}`.
