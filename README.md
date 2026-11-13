# WinterCare AI — Winter Health & Festival Safety Platform

An end-to-end educational project combining **Streamlit**, **FastAPI**, **Django Admin**, SQLAlchemy, SQLite/PostgreSQL and an explainable AI-assisted screening workflow.

## Features
- Streamlit command centre: KPIs, symptom screening, wellness guides, festival readiness, inventory and incident desk.
- FastAPI REST backend with validation, persistence and Swagger docs.
- Django admin portal for operational events, supplies and incident records.
- SQLite by default; PostgreSQL configurable through `DATABASE_URL`.
- Explainable screening score with transparent contributing factors. The optional scikit-learn dependency is included for future model experimentation; current screening uses deterministic, auditable rules.
- Demo data seeding.

> **Safety:** This is a portfolio/demo application, not a medical device. It does not diagnose, prescribe or replace a clinician. Use fictional data only. For severe breathing difficulty, chest pain, unconsciousness, confusion or another emergency, seek urgent medical care/contact emergency services (India: 112). Never delay care to use this app.

## Architecture

```text
Streamlit UI :8501 ──HTTP──> FastAPI :8000 ──SQLAlchemy──> SQLite / PostgreSQL
                                      ▲
Django Admin :8001 ──────────────────┘ (same database URL; Django owns django_* and ops tables)
```

## Quick start — Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# If activation is blocked:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env

python scripts\init_db.py
python scripts\seed_demo.py
```

Start each service in a separate terminal from the project root:

**Terminal 1 — API**
```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 — Streamlit**
```powershell
streamlit run frontend\app.py --server.port 8501
```

**Terminal 3 — Django admin (optional)**
```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8001
```

Open:
- Streamlit: http://127.0.0.1:8501
- FastAPI docs: http://127.0.0.1:8000/docs
- Django admin: http://127.0.0.1:8001/admin

## Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/init_db.py
python scripts/seed_demo.py
uvicorn backend.main:app --reload --port 8000
streamlit run frontend/app.py --server.port 8501
```

Run Django separately with `python manage.py migrate`, `python manage.py createsuperuser`, then `python manage.py runserver 127.0.0.1:8001`.

## PostgreSQL
Create a database, install `pip install "psycopg[binary]"`, then set:
```env
DATABASE_URL=postgresql+psycopg://wintercare:password@localhost:5432/wintercare
```
Run the database initialization and Django migrations again. SQLite requires no separate database server.

## REST API
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API health |
| GET | `/api/v1/dashboard` | KPI summary |
| POST/GET | `/api/v1/screenings` | Create/list screening records |
| POST/GET | `/api/v1/events` | Register/list events |
| POST/GET | `/api/v1/incidents` | Log/list incidents |
| POST/GET | `/api/v1/inventory` | Upsert/list supplies |
| GET | `/api/v1/wellness/{category}` | Winter wellness guide |

Swagger: `http://127.0.0.1:8000/docs`.

Example:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/screenings \
 -H "Content-Type: application/json" \
 -d '{"age":34,"temperature_c":37.8,"symptoms":["fever","persistent_cough"],"risk_conditions":[],"duration_days":2}'
```

## Project layout
```text
backend/             FastAPI, SQLAlchemy models, schemas and services
frontend/app.py      Streamlit multi-page command centre
django_portal/       Django settings, admin and operations models
scripts/             Database initialization and demo seeding
requirements.txt
.env.example
README.md
```

## Production readiness work
Before real-world use: clinical governance and independent validation, privacy/legal review, authentication/RBAC, audit logging, encryption, secrets management, backups, monitoring, rate limiting, secure deployment, consent and retention policies, and security testing. The screening and event readiness scores are illustrative heuristics, not clinical or regulatory standards.
