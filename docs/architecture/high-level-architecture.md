# High Level Architecture

### Technical Summary
The Universal Memory project will be a cross-platform desktop application built using the Tauri framework. The architecture follows a local client-server model, with the frontend UI built in React and a managed backend service running in Python. User data is stored exclusively on the user's machine in a hybrid database system, utilizing SQLite for structured metadata and ChromaDB for semantic vector search. The entire project will be managed within a single Monorepo to ensure cohesive development of the main application, browser extension, and any shared code. This local-first architecture prioritizes user privacy, data sovereignty, and high-performance interactions.

### Platform and Infrastructure Choice
**Platform:** The application is strictly **local-first** and will not rely on any cloud hosting or infrastructure for its core functionality. The target platforms are the user's desktop operating systems: Windows, macOS, and Linux, supported by the Tauri application framework.
**Key Services:**
* **Tauri:** Manages the desktop window, webview for the React UI, and the Python backend sidecar process.
* **Python Backend:** A local service responsible for all business logic, data processing, and database interactions.

### Repository Structure
**Structure:** Monorepo.
**Rationale:** The PRD recommends a Monorepo to effectively manage the multiple, distinct parts of the project (desktop app, browser extension, shared utilities) within a single repository, simplifying dependency management and ensuring consistency.

### High Level Architecture Diagram
```mermaid
graph TD
    subgraph User's Machine
        subgraph Browser
            A[AI Web App] -- User Interaction --> B[Browser Extension];
        end

        subgraph "Universal Memory App (Tauri)"
            C[React UI Frontend] -- User Interaction --> D[Python Backend Service];
        end

        subgraph "Local Storage"
            E[SQLite Database]
            F[ChromaDB]
        end

        B -- Captured Data --> D;
        D -- Read/Write --> E;
        D -- Read/Write/Search --> F;
    end