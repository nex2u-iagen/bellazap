# Frontend API Interactions

This document outlines the API interactions made by the frontend application, primarily identified within `frontend/src/App.tsx`. The frontend uses `axios` to communicate with the backend API.

## API Endpoints Consumed by Frontend (`frontend/src/App.tsx`)

The `App.tsx` component makes the following API calls to the backend:

-   `GET /api/v1/admin/help/{topic}`: Retrieves administration guides.
-   `PUT /api/v1/admin/agents/{id}`: Updates an existing AI agent configuration.
-   `POST /api/v1/admin/agents`: Creates a new AI agent configuration.
-   `POST /api/v1/admin/produtos/import`: Imports products from a CSV file.
-   `GET /api/v1/admin/stats`: Retrieves global admin statistics.
-   `GET /api/v1/admin/revendedoras`: Lists all resellers.
-   `GET /api/v1/admin/agents`: Lists all AI agent configurations.
-   `GET /api/v1/admin/agents/logs`: Lists AI agent message logs.
-   `DELETE /api/v1/admin/agents/{id}`: Deletes an AI agent.
-   `GET /api/v1/admin/financial/predictive`: Generates predictive financial insights.
-   `GET /api/v1/admin/configs`: Retrieves all system configurations.
-   `POST /api/v1/admin/configs`: Updates or creates a system configuration.
-   `POST /api/v1/admin/infra/evo/test`: Tests connectivity with the Evolution API.
-   `POST /api/v1/admin/infra/db/maintenance`: Runs database maintenance tasks.
