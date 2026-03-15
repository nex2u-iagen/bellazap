# Backend Deployment Configuration

This document outlines the deployment configuration for the backend application, primarily based on the `docker-compose.yml` file.

## `docker-compose.yml`

The `docker-compose.yml` file defines two core services:

### `db` service (PostgreSQL)
- **Image:** `postgres:16-alpine`
- **Restart Policy:** `always`
- **Environment Variables:**
  - `POSTGRES_DB`: `bellazap`
  - `POSTGRES_USER`: `postgres`
  - `POSTGRES_PASSWORD`: `postgres`
- **Ports:** `5432:5432` (host:container)
- **Volumes:** `pgdata:/var/lib/postgresql/data` (persisted data)

### `redis` service
- **Image:** `redis:7-alpine`
- **Restart Policy:** `always`
- **Ports:** `6379:6379` (host:container)
- **Volumes:** `redisdata:/data` (persisted data)

## Volumes
- `pgdata`: Used for PostgreSQL data persistence.
- `redisdata`: Used for Redis data persistence.

## Overall Architecture
The backend services are designed to run within Docker containers, utilizing PostgreSQL as the primary database and Redis for caching or task queue management.
