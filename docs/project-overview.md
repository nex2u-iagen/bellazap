# Project Overview

## Project Name
BellaZap

## Project Purpose
The BellaZap platform is a SaaS solution for cosmetics resellers, featuring WhatsApp automation, payment processing, product catalog management, and AI agent integration to streamline sales and support processes.

## Executive Summary
BellaZap is a multi-part application designed to empower cosmetics resellers. It comprises a Python FastAPI backend handling business logic, data storage, and external integrations (payments, WhatsApp, LLMs), and a React/TypeScript frontend providing an administrative interface. The system automates interactions via WhatsApp, manages a product inventory, processes financial transactions, and leverages AI agents for enhanced reseller support and sales.

## Technology Stack Summary

| Part      | Language   | Framework   | Key Libraries/Tools             | Database  | Task Queue |
| :-------- | :--------- | :---------- | :------------------------------ | :-------- | :--------- |
| **Backend** | Python     | FastAPI     | SQLAlchemy, Redis, Celery, Langchain | PostgreSQL | Celery     |
| **Frontend**| TypeScript | React       | Vite, Chakra UI, Axios          | N/A       | N/A        |

## Architecture Type Classification
-   **Repository Type**: Multi-part (with distinct backend and frontend applications)
-   **Backend Architecture**: Service-Oriented, API-centric
-   **Frontend Architecture**: Component-Based

## Repository Structure
The project is organized into two main parts within a single repository:
-   **`src/`**: Contains the Python FastAPI backend application.
-   **`frontend/`**: Contains the React/TypeScript frontend application.

## Links to Detailed Documentation

-   [Backend Architecture](./architecture-backend.md)
-   [Frontend Architecture](./architecture-frontend.md)
-   [Source Tree Analysis](./source-tree-analysis.md)
-   [Backend Data Models](./data-models-backend.md)
-   [Backend API Contracts](./api-contracts-backend.md)
-   [Frontend API Interactions](./api-interactions-frontend.md)
-   [Frontend UI Component Inventory](./ui-component-inventory-frontend.md)
-   [Development Guide](./development-guide.md)
-   [Deployment Guide](./deployment-guide.md)
-   [Integration Architecture](./integration-architecture.md)
