![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
"Retail AP"

A local data pipeline and visualization stack for monitoring retail transaction metrics. The system ingests simulated sales data, stores it in a normalized PostgreSQL database, exposes a validated REST API, and renders live KPIs and trend charts in a Streamlit dashboard.

Built to replace manual spreadsheet reporting with a queryable, reproducible analytics workflow.

## Architecture

```mermaid
graph LR
  Sim[Transaction Simulator] -->|HTTP POST /ingest| API[FastAPI Backend]
  DB[(PostgreSQL 15)] <-->|asyncpg Pool| API
  API -->|REST/JSON| UI[Streamlit Dashboard]
  UI -->|Auto-refresh| API

Tech Stack
Layer
Technology
Role
Database
PostgreSQL 15, asyncpg
Relational storage, FK constraints, parameterized queries
Backend
FastAPI, Uvicorn, Pydantic v2
Async REST API, payload validation, OpenAPI docs
Frontend
Streamlit, Plotly, Requests
Interactive dashboard, real-time visualization, state management
DevOps
Docker Compose, Git, .env
Local environment parity, reproducible setup
Testing/Seeding
Faker, psycopg2-binary
Realistic data generation, schema validation
Features
Normalized Schema: 4-table relational design with UUID primary keys, CHECK constraints, and cascading deletes.
Async API Layer: Connection pooling via asyncpg, Pydantic request/response models, and automatic OpenAPI documentation.
Live Ingestion: Simulator fetches valid foreign keys before posting, handles connection drops, and respects a 30-second cadence.
Dashboard UX: Custom CSS theming, date-range filtering, auto-refresh, and graceful fallbacks for missing data.
Containerized DB: One-command PostgreSQL setup with health checks and persistent volume mapping.
Quick Start
Prerequisites
Python 3.10+
Docker Desktop
Git
Setup
# 1. Clone & enter project
git clone https://github.com/Nirrmitt/retail-analytics-platform.git
cd retail-analytics-platform

# 2. Create virtual environment & install dependencies
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# 3. Start database
docker compose up -d

# 4. Apply schema & seed data
python database/force_create_tables.py
python database/seed_data.py

Run Services
Open three separate terminals:
Terminal 1: API Server

$env:PYTHONPATH = "."
uvicorn src.api.main:app --reload --port 8000

Terminal 2: Dashboard
streamlit run src/dashboard/app.py
Access:
Dashboard: http://localhost:8501
API Docs: http://localhost:8000/docs
Health Check: http://localhost:8000/health
Project Structure

├── database/               # DDL, seed scripts, diagnostic tools
├── scripts/                # Live data simulator
├── src/
│   ├── api/                # FastAPI routes, services, Pydantic models
│   ├── dashboard/          # Streamlit app, API client, components
│   └── config/             # Pydantic settings, environment management
├── .streamlit/             # Streamlit theme configuration
├── docker-compose.yml      # PostgreSQL container definition
├── requirements.txt        # Pinned Python dependencies
└── README.md

API Endpoints
Method
Path
Description
GET
/health
Database connectivity status
GET
/api/v1/kpi/revenue
Aggregated revenue, order count, AOV (configurable days)
GET
/api/v1/sales/daily-revenue
Timeseries data for trend charts
GET
/api/v1/sales/category-revenue
Category breakdown for bar charts
POST
/api/v1/data/ingest
Accepts transaction payloads, validates FKs, inserts atomically
All endpoints return JSON. Swagger UI at /docs provides interactive testing.
Data Ingestion Pipeline

The simulator (scripts/live_simulator.py) mimics production webhook behavior:
Queries the database at startup to fetch valid customer_id and product_id UUIDs.
Generates payloads with 1–3 line items per transaction.
POSTs to /api/v1/data/ingest with exponential backoff on connection failures.
Logs success/failure with timestamps for pipeline monitoring.
Foreign key validation ensures referential integrity. The API endpoint wraps inserts in a database transaction to prevent partial writes.
Development Notes
Windows Line Endings: PowerShell pipes and CRLF encoding can cause silent psql failures. The force_create_tables.py script bypasses file encoding issues by executing SQL over a direct psycopg2 connection.
Streamlit Caching: The dashboard uses st.rerun() and explicit cache clearing to reflect live data. The .streamlit/config.toml applies a consistent theme without modifying component code.
Port Conflicts: If 8000 or 5433 are occupied, update docker-compose.yml and the uvicorn command accordingly.
Import Paths: $env:PYTHONPATH = "." is required on Windows to resolve src.* imports when launching from the project root.
Production Considerations
This repository is structured for local development and portfolio demonstration. For production deployment:
Replace the simulator with actual e-commerce webhooks or a message broker (Kafka/RabbitMQ).
Add Redis caching for high-read KPI endpoints.
Implement JWT authentication and rate limiting on the ingestion route.
Switch uvicorn to a process manager (systemd, Docker Swarm, or Kubernetes).
Rotate database credentials via environment variables or a secrets manager.
License
MIT License. Free to use, modify, and reference in technical interviews or portfolio reviews.

