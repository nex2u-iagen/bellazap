---
stepsCompleted: [1]
inputDocuments:
  - docs/index.md
  - docs/project-overview.md
  - _evo-output/Telegram-conect/tech-spec-wip.md
  - docs/architecture-backend.md
workflowType: 'architecture'
project_name: 'BellaZap'
user_name: 'Eliezer'
date: '2026-03-15T15:22:00-03:00'
active_feature: 'Telegram-conect'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
- **Admin Full Management**: CRUD of representatives, plan management, and billing rules setup.
- **Shadow Login (Impersonation)**: Admin ability to view/interact with the representative's dashboard for support.
- **Reseller Operations**: Stock management, manual and automatic sales registration, and debt tracking.
- **Automated Billing (Asaas)**: Split payment logic using PIX, automatically charging platform fees based on the reseller's plan.
- **Unified Interface**: Full operations available via Web Panel and Telegram Bot (replacing WhatsApp).

**Non-Functional Requirements:**
- **Vercel Optimization**: All functions must be stateless and execute within Vercel Free limits (10s/request).
- **Data Persistence**: Use Turso (LibSQL) for reliable edge data storage.
- **Tenant Isolation**: Strict data segregation using `revendedora_id` at the query level.
- **AI Latency**: Use Groq/OpenAI for sub-second response times in conversational flows.

**Scale & Complexity:**
- **Primary domain**: Full-Stack (Web + Telegram Bot + FinTech API)
- **Complexity level**: Medium-High
- **Estimated architectural components**: 5 (Admin Web, Reseller Web, Telegram Bot Engine, Billing Engine, Data Layer)

### Technical Constraints & Dependencies
- **Vercel Free**: No persistent processes or local file storage.
- **Asaas API**: Integration for digital account, split payments, and PIX generation.
- **Turso/LibSQL**: Edge database for global low-latency access.

### Cross-Cutting Concerns Identified
- **Multi-tenancy Security**: Preventing data leakage between representatives.
- **Transaction Atomicity**: Ensuring stock is deducted only after a confirmed PIX sale.
- **Conversation State**: Managing complex flows in Telegram across serverless function restarts.

## Architectural Decisions & Refinement

### 1. Data Layer: Turso (LibSQL)
- **Rationale**: To operate within Vercel's serverless environment, we require a database that is persistent but edge-compatible. Turso provides the speed of SQLite with global replication.
- **Security**: Data isolation is enforced at the application level via `revendedora_id` mandatory filtering.

### 2. Financial Layer: Asaas Split Payment
- **Rationale**: Automates the complex task of commission splitting between the platform and the reseller.
- **Implementation**: Every sale triggers a PIX generation via Asaas. Upon confirmation, the split is executed automatically based on the representative's plan (Basic/Pro/Enterprise).

### 3. Interface: Telegram & Web Only
- **Rationale**: Eliminates the high maintenance and stateful nature of WhatsApp (Evolution API), allowing the backend to be purely event-driven and stateless.

### 4. AI Orchestration: Groq/OpenAI (Cloud-based)
- **Rationale**: Replaces local Ollama to fit within Vercel's 10-second request limit and reduces infrastructure requirements.

### 5. Summary of Consensus (Party Mode)
> "The project is moving towards a Maximum Efficiency / Minimum Cost model. Success depends on ultra-lean code execution and a seamless 'Wizard-style' UX on Telegram, turning technical complexity into an automatic profit engine."
