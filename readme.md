#  Retail Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> End-to-end retail intelligence: Production-grade PostgreSQL schema → Async FastAPI backend → Interactive Streamlit dashboard. Built with real-world architecture, not tutorials.

---

## System Architecture

```mermaid
graph LR
  DB[(PostgreSQL 15)] -->|asyncpg Pool| API[FastAPI Backend]
  API -->|REST/JSON| UI[Streamlit Dashboard]
  UI -->|User Filters| API
  API -->|Parameterized SQL| DB
  API -->|OpenAPI Spec| Docs[Swagger UI /docs]

  Key Features

 Normalized Database: 4-table relational schema with foreign keys, constraints, and materialized views for sub-100ms dashboard queries

 Async API Layer: FastAPI with asyncpg connection pooling, Pydantic validation, and auto-generated OpenAPI documentation

 Live Dashboard: Streamlit UI with Plotly charts, real-time KPIs, date-range filtering, and graceful error handling

 Production Patterns: Loading spinners, API health checks, request timeouts, and structured logging

 Business Metrics: Revenue tracking, Average Order Value (AOV), category performance, and order volume analytics

 Tech Stack
Layer
Technology
Purpose
Database
PostgreSQL 15, asyncpg
Relational storage, materialized views, parameterized queries
Backend
FastAPI, Uvicorn, Pydantic
Async REST API, data validation, auto-docs, type safety
Frontend
Streamlit, Plotly, Requests
Interactive dashboard, real-time visualization, state management
DevOps
Docker Compose, Git, Virtual Envs
Reproducible local setup, version control, dependency isolation

 Quick Start
Prerequisites
Python 3.10+
Docker & Docker Compose
Git
Setup & Run

# 1. Clone & navigate
git clone https://github.com/Nirrmitt/retail-analytics-platform.git
cd retail-analytics-platform

# 2. Start database container
docker compose up -d

# 3. Install dependencies & seed realistic sample data
pip install -r requirements.txt
python database/seed_data.py

# 4. Launch services (open two terminals)
# Terminal 1: API Server
uvicorn src.api.main:app --reload --port 8000

# Terminal 2: Dashboard
streamlit run src/dashboard/app.py

🔗 Interactive API Docs: http://localhost:8000/docs
🔗 Live Dashboard: http://localhost:8501

Project Structure

retail-analytics-platform/
├── database/               # Schema DDL, seed scripts, KPI SQL queries
├── src/
│   ├── api/                # FastAPI routes, services, Pydantic models
│   ├── dashboard/          # Streamlit app, API client, reusable components
│   └── config/             # Pydantic settings, environment management
├── tests/                  # Pytest suite (structured for CI/CD)
├── docs/                   # Architecture diagrams, screenshots, guides
├── docker-compose.yml      # Full-stack local environment
└── README.md               # You are here

 Dashboard Preview



 Business Value
This platform solves real retail operations challenges:
Revenue Visibility: Replaces manual Excel reporting with live, filterable dashboards
Category Optimization: Identifies high-margin products to guide marketing spend and inventory planning
Decision Speed: Parameterized API endpoints enable instant metric updates without database locks
Scalable Foundation: Designed to handle 1M+ transactions using connection pooling, materialized views, and async I/O

Planned Enhancements
Redis caching for high-traffic KPI endpoints
RFM customer segmentation & cohort retention analysis
Prophet/XGBoost sales forecasting with confidence intervals
GitHub Actions CI/CD pipeline with automated pytest coverage
PDF/CSV export functionality for stakeholder reporting

 Contributing
Fork the repository
Create a feature branch (git checkout -b feat/your-feature)
Commit changes (git commit -m 'feat: add inventory turnover metric')
Push to branch (git push origin feat/your-feature)
Open a Pull Request with a clear description and test results
See CONTRIBUTING.md for detailed guidelines.
📄 License & Contact
📄 License: MIT — Free for portfolio, learning, and commercial use
👤 Built by: Nirrmitt
🔗 Connect: LinkedIn