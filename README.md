# Kumo – FinOps Platform

High-performance FinOps platform backend (FastAPI, PostgreSQL, Celery, Redis).

## Quick start with Docker

```bash
docker-compose up -d
```

- **API:** http://localhost:8000  
- **Docs:** http://localhost:8000/docs  
- **Health:** http://localhost:8000/health  

Services: `web` (FastAPI), `worker` (Celery), `db` (PostgreSQL 15), `redis`.

## Local development

1. Copy env and start DB/Redis:

   ```bash
   copy .env.example .env
   docker-compose up -d db redis
   ```

2. Create a virtualenv and run the app:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

## Project structure

```
app/
├── main.py           # FastAPI app, health, lifespan
├── core/
│   └── config.py     # Pydantic-settings (DB_URL, REDIS_URL, etc.)
├── db/
│   ├── base.py       # SQLAlchemy Base
│   └── session.py    # Async engine & session
├── api/v1/           # API routes (versioned)
└── workers/          # Celery app & tasks
```

## Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_URL` | PostgreSQL URL (use `postgresql+asyncpg://`) | `postgresql+asyncpg://kumo:kumo@localhost:5432/kumo` |
| `REDIS_URL` | Redis URL | `redis://localhost:6379/0` |
| `ENVIRONMENT` | `development` \| `staging` \| `production` | `development` |
