# Development Guide

This document outlines the development setup, installation steps, environment configuration, and common commands for both the backend and frontend parts of the project.

## 1. Backend Development

### Prerequisites
-   **Python**: Version 3.x (as per `requirements.txt`)
-   **PostgreSQL**: Database server (configured via `docker-compose.yml`)
-   **Redis**: In-memory data store (configured via `docker-compose.yml`)
-   **Docker & Docker Compose**: For running database and Redis services locally.

### Installation Steps
1.  **Clone the repository**: `git clone <repository_url>`
2.  **Navigate to the project root**: `cd BellaZap`
3.  **Create a Python virtual environment**: `python -m venv .venv`
4.  **Activate the virtual environment**:
    -   Windows: `.\.venv\Scripts\activate`
    -   Linux/macOS: `source ./.venv/bin/activate`
5.  **Install Python dependencies**: `pip install -r requirements.txt`
6.  **Start Docker services**: `docker-compose up -d` (starts PostgreSQL and Redis)

### Environment Setup
-   Copy `.env.example` to `.env` and fill in the necessary environment variables.
    -   `SECRET_KEY` for JWT.
    -   Database credentials (matching `docker-compose.yml`).
    -   API keys for external services (Asaas, Abacate, WhatsApp, OpenAI).
-   Configuration is managed in `src/core/config.py` using Pydantic Settings.

### Run Commands
-   **Start the FastAPI application (development mode)**: `uvicorn src.main:app --reload`
-   **Start all services (FastAPI, Celery workers) locally with Honcho**: `honcho start` (requires `Procfile.dev`)

### Test Commands
-   **Run all tests**: `pytest`

### Database Migrations
-   Alembic is used for database migrations.
-   `alembic.ini`: Alembic configuration file.
-   Commands typically include `alembic revision --autogenerate -m "description"` and `alembic upgrade head`.

## 2. Frontend Development

### Prerequisites
-   **Node.js**: (Version specified in `package.json` or project guidelines, usually latest LTS)
-   **npm** or **Yarn**: Package manager for Node.js.

### Installation Steps
1.  **Navigate to the frontend directory**: `cd frontend`
2.  **Install Node.js dependencies**: `npm install` (or `yarn install`)

### Environment Setup
-   Vite manages environment variables prefixed with `VITE_` via `.env` files in the frontend directory.
-   Ensure the backend is running for API interactions. The `vite.config.ts` proxies API requests to `http://localhost:8000`.

### Build Commands
-   **Build for production**: `npm run build` (executes `tsc && vite build`)

### Run Commands
-   **Start the development server**: `npm run dev` (executes `vite`)

### Test Commands
-   **Run linting checks**: `npm run lint` (executes `eslint`)
-   No explicit separate unit/integration test command was found in `package.json`. Testing is likely integrated with the build process or performed manually.
