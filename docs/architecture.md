# Universal Memory Fullstack Architecture Document

## High Level Architecture
The architecture is a local client-server model within a cross-platform Tauri desktop application. A React frontend communicates with a managed Python backend service. Data is stored locally in a hybrid SQLite and ChromaDB system. The entire project is a monorepo.

## Tech Stack
| Category | Technology | Version |
| :--- | :--- | :--- |
| Desktop Framework | Tauri | 2.0 (beta) |
| Monorepo Tool | npm Workspaces| 10.x |
| Frontend | React, TypeScript, Vite | 18.x, 5.x, 5.x |
| Styling | Tailwind CSS | 3.x |
| State Management | Zustand | 4.x |
| Backend | Python, FastAPI | 3.11, 0.11x.x |
| Database | SQLite & ChromaDB | Latest |
| Testing | Playwright, Vitest, pytest | Latest |

## API Specification
A local RESTful API is defined with OpenAPI 3.0, providing endpoints for managing and searching conversations (e.g., `POST /conversations`, `GET /conversations`, `POST /search`).

## Unified Project Structure
```plaintext
universal-memory/
├── apps/
│   ├── desktop/
│   ├── extension/
│   └── api/
├── packages/
│   ├── shared-types/
└── package.json