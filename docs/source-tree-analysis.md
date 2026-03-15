# Source Tree Analysis

This document provides an annotated overview of the project's directory structure, highlighting critical folders, entry points, and the organization of both backend and frontend components.

## Project Structure Overview

The project is structured as a **multi-part** application, consisting of a Python FastAPI backend and a React/TypeScript frontend.

```
BellaZap/
├── alembic/                    # SQLAlchemy Alembic migrations for database schema management.
│   ├── versions/               # Individual migration scripts.
│   └── ...
├── src/                        # Main backend application source code (Python).
│   ├── api/                    # API endpoint definitions.
│   │   ├── v1/                 # Version 1 of the API.
│   │   │   ├── endpoints/      # Contains endpoint modules.
│   │   │   │   ├── admin.py    # Admin-related API endpoints.
│   │   │   │   ├── agents.py   # AI Agent interaction endpoints.
│   │   │   │   ├── payments.py # Payment-related API endpoints.
│   │   │   │   └── whatsapp.py # WhatsApp integration API endpoints.
│   │   └── ...
│   ├── core/                   # Core utilities and configurations.
│   │   ├── config.py           # Application settings and environment variables (including JWT secrets).
│   │   ├── monitoring.py       # Monitoring related utilities.
│   │   └── ...
│   ├── db/                     # Database connection and session management.
│   │   ├── base.py             # Base class for SQLAlchemy declarative models.
│   │   ├── session.py          # Database session handling (AsyncSessionLocal).
│   │   └── ...
│   ├── domains/                # Business logic organized by domain.
│   │   ├── agentes/            # AI Agents domain logic.
│   │   ├── notificacoes/       # Notification domain logic.
│   │   ├── pagamentos/         # Payment domain logic.
│   │   │   ├── providers/      # Payment provider integrations (e.g., Asaas, Abacate).
│   │   │   ├── split_calculator/# Logic for payment splitting.
│   │   │   └── ...
│   │   ├── revendedoras/       # Reseller domain logic.
│   │   ├── whatsapp/           # WhatsApp integration domain logic.
│   │   └── ...
│   ├── models/                 # SQLAlchemy ORM models (database schema definitions).
│   │   ├── core.py             # Core application models (e.g., Revendedora, Venda).
│   │   ├── payment.py          # Payment-related models (e.g., Transaction, PaymentProvider).
│   │   └── ...
│   ├── schemas/                # Pydantic schemas for API request/response validation and data serialization.
│   │   └── ...
│   ├── services/               # Placeholder for service layer logic (currently empty).
│   │   └── ...
│   ├── workers/                # Celery workers for asynchronous tasks.
│   │   ├── reconciliation_worker.py # Worker for payment reconciliation and webhook retries.
│   │   └── ...
│   ├── main.py                 # Backend application entry point (FastAPI app definition).
│   └── ...
├── tests/                      # Unit and integration tests for the backend.
│   └── ...
├── frontend/                   # Frontend application source code (React/TypeScript).
│   ├── src/                    # Main frontend source.
│   │   ├── features/           # UI components organized by feature.
│   │   │   ├── admin/          # Admin-specific UI components (`AdminManagement.tsx`, `PagamentosMonitor.tsx`).
│   │   │   ├── auth/           # Authentication-related UI components (`AdminLogin.tsx`, `Login.tsx`).
│   │   │   ├── revendedora/    # Reseller-specific UI components (`Financeiro.tsx`).
│   │   │   └── ...
│   │   ├── App.tsx             # Main application component, handles routing and API interactions.
│   │   ├── index.css           # Global CSS styles.
│   │   ├── main.tsx            # Entry point for the React application.
│   │   ├── theme.ts            # Chakra UI theme configuration.
│   │   └── ...
│   ├── public/                 # Static assets (e.g., index.html, images).
│   ├── node_modules/           # Node.js dependencies.
│   ├── package.json            # Node.js dependencies and project metadata.
│   ├── package-lock.json       # Locked Node.js dependencies.
│   ├── vite.config.ts          # Vite build and development server configuration (includes API proxy).
│   └── ...
├── .env                        # Environment variables (local).
├── .env.example                # Example environment variables.
├── .gitignore                  # Git ignore rules.
├── alembic.ini                 # Alembic configuration file.
├── docker-compose.yml          # Docker Compose configuration for local development (database, Redis).
├── Procfile.dev                # Process file for local development (e.g., for Honcho).
├── pytest.ini                  # Pytest configuration.
├── README.md                   # Project overview and basic setup instructions.
├── requirements.txt            # Python dependencies.
├── run.py                      # Script to run the application (e.g., starting backend server or workers).
└── start.bat                   # Windows batch script to start the application.
```
