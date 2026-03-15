# Backend Architecture Document

## 1. Executive Summary

The backend of the BellaZap application is a Python-based FastAPI service designed to provide core business logic, manage data, expose API endpoints for the frontend, and integrate with various external services. It handles reseller management, product catalog, sales tracking, payment processing, AI agent interactions, and WhatsApp communications.

## 2. Technology Stack

-   **Language**: Python 3.x
-   **Web Framework**: FastAPI
-   **Asynchronous ORM**: SQLAlchemy with AsyncPG driver
-   **Database**: PostgreSQL
-   **Task Queue**: Celery
-   **Message Broker/Backend for Celery**: Redis
-   **Dependency Management**: `pip` with `requirements.txt`
-   **Environment Management**: `python-dotenv`, Pydantic Settings
-   **API Clients**: `httpx`, `axios` (for external services, implicitly)
-   **AI/LLM Integration**: Langchain (for Agent functionalities)

## 3. Architecture Pattern

The backend follows a **Service-Oriented Architecture (SOA)** with a strong **API-centric** design. Key characteristics include:
-   **Layered Structure**: Separation of concerns with distinct layers for API endpoints, business logic (domains), data access (repositories, ORM models), and core utilities.
-   **Asynchronous Operations**: Leverages Python's `async/await` and `FastAPI`'s asynchronous capabilities for non-blocking I/O.
-   **Background Tasks**: Uses `Celery` and `Redis` for handling long-running or periodic tasks (e.g., payment reconciliation, webhook retries).
-   **Domain-Driven Design (DDD) principles**: Business logic is organized into distinct `domains` (e.g., `pagamentos`, `whatsapp`, `agentes`).

## 4. Data Architecture

-   **Database**: PostgreSQL
-   **ORM**: SQLAlchemy 2.0+ (asynchronous mode)
-   **Migration Tool**: Alembic
-   **Data Models**: Defined using SQLAlchemy declarative models in `src/models/`. Key models include:
    -   `Revendedora`: Reseller information.
    -   `Venda`: Sales records.
    -   `Produto`: Global product catalog.
    -   `Transaction`: Detailed payment transactions.
    -   `PaymentProvider`: Configuration for payment gateways.
    -   `AgentConfig`, `MessageLog`, `SystemConfiguration`: For AI agent and system-wide settings.
    -   (Refer to `data-models-backend.md` for a comprehensive list and details).

## 5. API Design

-   **Type**: RESTful API
-   **Framework**: FastAPI (provides automatic OpenAPI/Swagger documentation).
-   **Version Control**: API endpoints are namespaced under `/api/v1/`.
-   **Endpoint Categories**: Endpoints are logically grouped into routers for:
    -   `payments`: Payment creation and processing.
    -   `admin`: Administrative tasks, statistics, reseller management, configurations, product import, infrastructure testing, agent management.
    -   `agents`: AI agent interaction (e.g., chat).
    -   `whatsapp`: WhatsApp integration webhooks and messaging.
-   **Data Validation/Serialization**: Handled by Pydantic schemas (`src/schemas/`) ensuring strong typing and automatic validation for request and response bodies.
-   **Authentication**: Implemented using **JWT (JSON Web Tokens)**, with configuration settings (`SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `ALGORITHM`) defined in `src/core/config.py`. Specific endpoints would require valid JWT tokens for access.
-   (Refer to `api-contracts-backend.md` for a comprehensive list of endpoints, request/response structures, and descriptions).

## 6. Component Overview

-   **`src/main.py`**: The application's entry point, initializes the FastAPI app and includes API routers.
-   **`src/api/v1/endpoints/`**: Contains Python modules defining specific API routes for different functional areas.
-   **`src/core/`**: Shared core functionalities and configurations (e.g., `config.py` for settings, `monitoring.py`).
-   **`src/db/`**: Database utilities, including SQLAlchemy session management and base model definitions.
-   **`src/domains/`**: Business logic components, encapsulating domain-specific operations (e.g., `PaymentService`, `WhatsAppService`, `BellaAgent`).
-   **`src/models/`**: SQLAlchemy ORM models defining the database schema.
-   **`src/schemas/`**: Pydantic models for data validation and serialization.
-   **`src/workers/`**: Celery workers (e.g., `reconciliation_worker.py`) for processing background tasks.

## 7. Source Tree

-   The detailed directory structure and annotations are provided in `source-tree-analysis.md`.

## 8. Development Workflow

-   **Local Setup**: Utilizes Python virtual environments, `pip` for dependencies, and `docker-compose` for local database (PostgreSQL) and message broker (Redis) services.
-   **Running Application**: FastAPI development server (`uvicorn`) or `honcho` for multi-process orchestration (`Procfile.dev`).
-   **Database Migrations**: Managed via Alembic.
-   (Refer to `development-guide.md` for detailed instructions).

## 9. Deployment Architecture

-   **Containerization**: `docker-compose.yml` configures essential services (PostgreSQL, Redis). The main FastAPI application's containerization (Dockerfile) is not explicitly defined in the project root but would typically involve building a Docker image for the application.
-   **Process Management**: `Procfile.dev` indicates how multiple processes (FastAPI, Celery) are orchestrated.
-   **CI/CD**: No explicit CI/CD pipelines were found, suggesting manual deployment or external CI/CD tool usage.
-   (Refer to `deployment-guide.md` for more details).

## 10. Testing Strategy

-   **Framework**: Pytest
-   **Configuration**: `pytest.ini`
-   Tests are located in the `tests/` directory.
-   Includes unit and integration tests.
