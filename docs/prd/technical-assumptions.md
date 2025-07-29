# Technical Assumptions

### Repository Structure: Monorepo
The project will be structured as a Monorepo to cohesively manage the various components like the desktop app, browser extension, and any future IDE extensions.

### Service Architecture
The application will use a local client-server model. The Tauri shell, built with React, will act as the client application. The Python-based Memory Core will run as a managed local service that the client communicates with.

### Testing Requirements
A Full Testing Pyramid approach is recommended, including Unit, Integration, and End-to-End (E2E) tests to ensure robustness across the system.

### Additional Technical Assumptions and Requests
* **Core Application Framework**: The cross-platform desktop application will be built using **Tauri**.
* **Frontend UI Framework**: The user interface for the dashboard will be built using **React**.
* **Backend Language**: The Memory Core and all backend logic will be written in **Python**.
* **Database Solution**: A hybrid approach will be used: **SQLite** for structured metadata and **ChromaDB** for local semantic vector search.
* **Deployment & Hosting**: No external hosting is required. The application is strictly **local-first**.