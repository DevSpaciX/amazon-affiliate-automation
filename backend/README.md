# Backend

FastAPI-based service implementing affiliate automation pipeline.

## Stack

- FastAPI
- Async SQLAlchemy
- SQLite
- Adapter pattern

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env


uvicorn app.main:app --reload --port 8000
```

## API
POST /api/links

GET /r/{code}

POST /api/simulate-buy

GET /api/transactions

GET /api/commission-rates

## Design
Service layer + Amazon adapter abstraction allow switching mock → live.