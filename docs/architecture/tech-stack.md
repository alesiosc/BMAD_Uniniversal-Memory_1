# Tech Stack

### Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Desktop Framework** | Tauri | 2.0 (beta) | Core framework for the cross-platform desktop application. | Provides a secure, lightweight, and performant webview-based shell with native OS integration. |
| **Monorepo Tool** | npm Workspaces| 10.x | Manages the frontend, backend, and shared packages in one repository. | Built-in to Node.js/npm, lightweight, and sufficient for our project's scale. |
| **Frontend Language**| TypeScript | 5.x | Primary language for the React frontend. | Adds static typing for improved maintainability and developer experience. |
| **Frontend Framework**| React | 18.x | UI library for building the dashboard interface. | Specified in the PRD; a robust and popular choice with a vast ecosystem. |
| **UI Styling** | Tailwind CSS | 3.x | Utility-first CSS framework for styling components. | Enables rapid, consistent styling that aligns with the minimalist aesthetic. |
| **State Management**| Zustand | 4.x | Lightweight state management for the React frontend. | Simple, unopinionated, and less boilerplate than other solutions like Redux. |
| **Frontend Testing**| Vitest / Playwright| Latest | Unit/Integration (Vitest) and End-to-End (Playwright) testing. | Vitest integrates seamlessly with Vite. Playwright offers robust E2E testing for Tauri apps. |
| **Build Tool** | Vite | 5.x | Build tool and dev server for the React frontend. | Extremely fast performance for a superior developer experience. |
| **Backend Language**| Python | 3.11 | Primary language for the local backend service. | Specified in the PRD; excellent for data processing and a vast ML/AI ecosystem. |
| **Backend Framework**| FastAPI | 0.11x.x| Framework for building the local RESTful API. | High-performance, easy to use, and includes automatic API documentation. |
| **Database** | SQLite & ChromaDB | Latest | Hybrid database solution for local storage. | SQLite for structured metadata; ChromaDB for efficient semantic vector search, as per the PRD. |
| **Backend Testing**| pytest | 8.x | Testing framework for the Python backend. | The de-facto standard for Python testing; powerful and extensible. |