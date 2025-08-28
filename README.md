# Django Job Tool — Starter

A minimal Django app for tracking projects, work entries (assets & hours), materials with markup, payments, and a per-project report.

## Local quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate --run-syncdb
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000 and /admin.

## Deploy on Render
- Push this repo to GitHub.
- In Render: New → Blueprint → select repo (uses render.yaml).
- After deploy: Shell → `python manage.py createsuperuser`.

## Data model
Customers → Clients → Projects (with material markup %) → WorkEntries, MaterialEntries, Payments.
Per-project rate overrides supported.
