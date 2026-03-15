# Frontend Architecture Document

## 1. Executive Summary

The frontend of the BellaZap application is a modern single-page application (SPA) built with React and TypeScript. Its primary role is to provide a user-friendly administrative interface for managing various aspects of the BellaZap platform, including resellers, payments, AI agents, and WhatsApp integrations, by interacting with the backend API.

## 2. Technology Stack

-   **Language**: TypeScript
-   **JavaScript Library**: React
-   **Build Tool**: Vite
-   **UI Component Library**: Chakra UI
-   **Routing**: React Router DOM
-   **HTTP Client**: Axios
-   **Package Manager**: npm (or Yarn)

## 3. Architecture Pattern

The frontend follows a **Component-Based Architecture**, which is standard for modern React applications.
-   **Modular Structure**: Components are organized by feature (`features/admin`, `features/auth`, `features/revendedora`).
-   **Declarative UI**: React's declarative paradigm is used to build interactive user interfaces.
-   **Client-Side Routing**: Handled by React Router DOM for seamless navigation without full page reloads.

## 4. Data Architecture

-   The frontend does not directly interact with a database. It consumes and presents data exclusively via the **RESTful API exposed by the backend**.
-   Data models are implicitly derived from the backend's Pydantic schemas, which define the structure of API requests and responses.
-   State management appears to be handled locally within components using React's built-in state hooks (e.g., `useState`, `useReducer`) and prop drilling, as no explicit global state management library (like Redux, Context API) was found.

## 5. API Design

-   **Type**: Consumes RESTful API
-   **HTTP Client**: Axios
-   **Endpoints Consumed**: The frontend interacts with a wide range of backend endpoints for administrative tasks, authentication, and feature-specific operations. These include `/api/v1/admin/*`, `/api/v1/payments/*`, `/api/v1/agents/*`, and `/api/v1/whatsapp/*`.
-   **Authentication**: Expects JWT tokens from the backend for authenticated requests, typically sent in the `Authorization` header.
-   (Refer to `api-interactions-frontend.md` for a comprehensive list of consumed endpoints and their details).

## 6. Component Overview

-   **`frontend/src/App.tsx`**: The main application component, responsible for overall layout, routing setup, and high-level API interactions.
-   **`frontend/src/main.tsx`**: The entry point for the React application, responsible for rendering the root `App` component.
-   **`frontend/src/features/`**: Contains subdirectories for distinct features, each housing relevant UI components:
    -   `admin/`: Components for managing administrative tasks (e.g., `AdminManagement.tsx`, `PagamentosMonitor.tsx`).
    -   `auth/`: Components for user authentication (e.g., `AdminLogin.tsx`, `Login.tsx`).
    -   `revendedora/`: Components specific to reseller functionalities (e.g., `Financeiro.tsx`).
-   **`frontend/src/theme.ts`**: Configuration file for Chakra UI, defining the application's visual theme.
-   (Refer to `ui-component-inventory-frontend.md` for a detailed list of identified UI components).

## 7. Source Tree

-   The detailed directory structure and annotations are provided in `source-tree-analysis.md`.

## 8. Development Workflow

-   **Local Setup**: Requires Node.js and npm/Yarn. Dependencies are managed via `package.json`.
-   **Running Application**: Uses `Vite`'s development server (`npm run dev`) with Hot Module Replacement (HMR).
-   **Build Process**: `npm run build` command compiles TypeScript and bundles assets for production.
-   (Refer to `development-guide.md` for detailed instructions).

## 9. Deployment Architecture

-   **Build Output**: The `npm run build` command generates static assets that can be served by any static file server.
-   **Serving Strategy**: Typically deployed as static files to a CDN or a web server, or integrated into the backend application to be served directly.
-   `frontend/vite.config.ts` includes development-specific configurations like a proxy for API calls.
-   (Refer to `deployment-guide.md` for more details).

## 10. Testing Strategy

-   **Linting**: `eslint` is configured and run via `npm run lint` for code quality and style enforcement.
-   No explicit separate unit or integration test framework setup (like Jest, React Testing Library) was identified in `package.json` or project files. Testing is likely performed manually or through integrated development practices.
