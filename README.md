# Habit Tracker — AI Code Review & Testing

A lightweight FastAPI + SQLite service for tracking daily habits and check-ins, developed with agentic workflows, deterministic guardrails (`black`, `ruff`, `pytest`), and AI-assisted PR reviews.

---

## Setup & Installation

```bash
pip install -r requirements.txt
```

---

## Running the Guardrails

We enforce deterministic guardrails before every commit and in CI:

```bash
# 1. Format check
black --check .

# 2. Lint check
ruff check .

# 3. Unit test suite
pytest

# Or run all guardrails with one command:
chmod +x check.sh
./check.sh
```

---

## Running the Application

```bash
uvicorn main:app --reload
```
Interactive API docs are available at `http://localhost:8000/docs`.

---

## Endpoints
- `POST /habits` — Create a new habit (`{"name": "Read 20 mins"}`)
- `GET /habits` — List all habits
- `POST /habits/{id}/checkin` — Record daily check-in (`{"day": "2026-11-06"}`)
- `GET /habits/{id}/checkins` — List all check-ins for a habit
- `GET /habits/{id}/streak` — Get current streak of consecutive days
