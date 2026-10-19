# Backend

Main REST API. It handles users and roles, tests, answers and results,
and calls the speech and LLM services.

Run:

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Folders:

| Folder | What is inside |
| --- | --- |
| `app/routers/` | API endpoints |
| `app/models/` | Database models |
| `app/services/` | Business logic |
