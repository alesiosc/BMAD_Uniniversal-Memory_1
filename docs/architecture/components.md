# Components

### Browser Extension
* **Responsibility:** This component is solely responsible for detecting user interactions on supported AI websites, capturing the conversation content (prompts and responses), and forwarding this data to the local Python Backend Service via the API.
* **Key Interfaces:** Exposes no public interfaces. It acts as a client to the `/conversations` POST endpoint on the backend.
* **Dependencies:** Python Backend Service.
* **Technology Stack:** Standard Web Extension technologies (JavaScript, HTML, CSS).

### React UI Frontend
* **Responsibility:** This is the user-facing part of the desktop application. It is responsible for rendering all views (Dashboard, Search, Settings, etc.), managing user input, and displaying data fetched from the backend.
* **Key Interfaces:** Provides the graphical user interface for the user. Acts as a client to all endpoints of the Python Backend Service.
* **Dependencies:** Python Backend Service.
* **Technology Stack:** Tauri, React, TypeScript, Tailwind CSS, Zustand.

### Python Backend Service
* **Responsibility:** The core engine of the application. It handles all business logic, including receiving data from the extension, generating embeddings, writing to and reading from the databases, and executing searches. It exposes the RESTful API for the other components to consume.
* **Key Interfaces:** Exposes the RESTful API defined in the previous section.
* **Dependencies:** SQLite Database, ChromaDB.
* **Technology Stack:** Python, FastAPI, SQLite, ChromaDB.