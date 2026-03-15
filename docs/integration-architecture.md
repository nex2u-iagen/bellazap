# Integration Architecture

This document describes how the different parts of the BellaZap project (backend and frontend) integrate and communicate with each other.

## 1. Overview

The BellaZap project is a multi-part application consisting of a Python FastAPI backend and a React/TypeScript frontend. The primary mode of communication between these two parts is through a **RESTful API** exposed by the backend and consumed by the frontend.

## 2. Integration Points

### Frontend to Backend (REST API)

-   **From**: Frontend (`frontend/`)
-   **To**: Backend (`src/`)
-   **Type**: REST API over HTTP/HTTPS
-   **Details**:
    -   The frontend (developed with React/TypeScript and built with Vite) makes HTTP requests to various API endpoints exposed by the FastAPI backend.
    -   During development, the Vite development server proxies requests starting with `/api` to `http://localhost:8000`, where the backend is expected to be running.
    -   For production deployments, the frontend typically makes direct requests to the backend API's URL.
    -   **API Endpoints Consumed**: The frontend interacts with a wide range of backend endpoints, primarily under the `/api/v1/admin/`, `/api/v1/payments/`, `/api/v1/agents/`, and `/api/v1/whatsapp/` prefixes. Specific endpoints are detailed in `api-interactions-frontend.md`.
    -   **Authentication Flow**: While explicit authentication implementation details were not fully scanned, the presence of `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, and `ALGORITHM` in the backend's `src/core/config.py` strongly suggests the use of **JWT (JSON Web Token) based authentication**. The frontend would typically store these tokens (e.g., in `localStorage` or `sessionStorage`) and send them in the `Authorization` header of subsequent requests to authenticated backend endpoints.

### Backend to External Services

The backend also integrates with several external services:

-   **Payment Providers**: (e.g., Asaas, Abacate Pay)
    -   **Type**: External REST APIs.
    -   **Details**: The backend makes outbound calls to these providers for payment processing, status checks, and receives inbound webhooks for transaction updates.
-   **WhatsApp (Evolution API or similar)**:
    -   **Type**: External REST API.
    -   **Details**: The backend interacts with the WhatsApp API for sending messages, creating instances, and receiving inbound webhooks for message events.
-   **LLM Providers (OpenAI, Ollama)**:
    -   **Type**: External APIs.
    -   **Details**: The backend communicates with Large Language Models for AI agent functionalities, configurable for local (Ollama) or cloud (OpenAI) providers.

## 3. Data Flow

-   **Frontend to Backend**: User actions on the frontend trigger API calls to the backend, sending request data (e.g., JSON payloads for creating payments, updating agent configurations).
-   **Backend to Database**: The backend processes requests, interacts with the PostgreSQL database (via SQLAlchemy ORM) for data storage and retrieval.
-   **Backend to External Services**: The backend communicates with external APIs for core functionalities like payments and WhatsApp messaging.
-   **Webhooks**: External services (e.g., payment providers, WhatsApp API) send asynchronous notifications (webhooks) back to the backend to update transaction statuses or message events.

## 4. Shared Data / Contracts

-   **Pydantic Schemas**: The backend defines Pydantic schemas (`src/schemas/`) which serve as clear contracts for API request and response data structures. These implicitly guide frontend developers on expected data formats.
-   **Database Schema**: Defined by SQLAlchemy models (`src/models/`), representing the persistent data structure.

## 5. Integration Architecture Diagram (Conceptual)

```mermaid
graph TD
    A[Frontend: React/Vite] -->|HTTP Requests (Axios)| B(Backend: FastAPI)
    B -->|SQLAlchemy ORM| C[Database: PostgreSQL]
    B -->|Celery Tasks| D(Task Queue: Redis)
    D --> B
    B -->|API Calls| E[External Service: Payment Provider]
    E -->|Webhooks| B
    B -->|API Calls| F[External Service: WhatsApp API]
    F -->|Webhooks| B
    B -->|API Calls| G[External Service: LLM Provider]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#afa,stroke:#333,stroke-width:2px
    style E fill:#ffc,stroke:#333,stroke-width:2px
    style F fill:#ffc,stroke:#333,stroke-width:2px
    style G fill:#ffc,stroke:#333,stroke-width:2px
```
