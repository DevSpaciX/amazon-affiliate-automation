# Amazon Affiliate Automation System

End-to-end automation pipeline for Amazon affiliate workflow:

- link generation
- redirect tracking
- transaction verification
- revenue calculation
- accounting dashboard

---

## Architecture

Frontend (Vue + Vuetify)
↓
FastAPI API
↓
Service layer
↓
Amazon Adapter (mock/live)
↓
SQLite

yaml
Копировать код

System designed to support mock execution and real Amazon PA-API/report ingestion.

---

## Demo flow

1. Generate affiliate link
2. Open redirect
3. Simulate purchase
4. Observe transaction in dashboard

---

## Run locally

See:

- backend/README.md
- frontend/README.md
