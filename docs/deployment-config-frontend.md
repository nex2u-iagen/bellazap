# Frontend Deployment Configuration

This document outlines the deployment-related configuration for the frontend application, primarily based on the `vite.config.ts` file.

## `vite.config.ts`

The `vite.config.ts` file primarily configures the development server and build process for the React application.

-   **Plugins**: Uses `@vitejs/plugin-react` for React support.
-   **Development Server (`server`)**:
    -   **`port`**: `5173` (Frontend development server runs on port 5173).
    -   **`proxy`**: Configured to proxy requests from `/api` to `http://localhost:8000`. This means that during development, API calls from the frontend to `/api` will be redirected to the backend server running on port 8000.

## Deployment Strategy (Inferred)

Given the absence of explicit deployment files like `Dockerfile` or CI/CD configurations within the frontend directory, the deployment strategy is inferred to be one of the following:

-   **Static Site Deployment**: The built frontend assets (from `vite build`) are deployed as static files to a web server (e.g., Nginx, Apache) or a CDN.
-   **Backend-served**: The built frontend assets are served directly by the backend application (FastAPI in this case), possibly by placing them in a static files directory within the backend.

The proxy configuration in `vite.config.ts` is crucial for local development, ensuring seamless communication between the frontend development server and the running backend API.
