# Epic 1: Foundation & Core Capture

**Goal:** This epic focuses on establishing the complete technical foundation of the Universal Memory application. By the end of this epic, we will have a runnable desktop application and a functional browser extension that can automatically capture a user's AI conversations from a web browser and securely save them to a local database. This delivers the first piece of core value: seamless, automated memory capture.

### Story 1.1: Project Scaffolding and Application Entrypoint
**As an** AI Power User,
**I want** to install and launch the basic Universal Memory application,
**so that** the foundational framework for my external brain is in place.

**Acceptance Criteria:**
1.  A monorepo project structure is created and initialized.
2.  A basic, empty Tauri desktop application can be successfully built and launched.
3.  A basic Python backend service is established and can be launched as a sidecar by the Tauri application.
4.  A basic communication channel is established, allowing the Tauri frontend to confirm the Python backend is running (e.g., a health check).

### Story 1.2: Local Database Initialization
**As an** AI Power User,
**I want** the application to initialize the local databases on its first run,
**so that** my captured memories have a secure and persistent place to be stored.

**Acceptance Criteria:**
1.  On first launch, the application creates the necessary SQLite and ChromaDB database files in a designated local directory.
2.  The Python backend service can successfully establish and manage connections to both databases.
3.  The required tables and schemas for storing conversation metadata are created in the SQLite database.
4.  A collection for storing vector embeddings is successfully initialized in ChromaDB.

### Story 1.3: Browser Extension for Web Capture
**As an** AI Power User,
**I want** to install a browser extension that automatically detects and captures my conversations with AI web apps,
**so that** my interactions are saved without any manual effort.

**Acceptance Criteria:**
1.  A functional browser extension for Chrome is created.
2.  The extension correctly identifies when the user is interacting with a supported AI web platform (e.g., ChatGPT).
3.  The user's prompts and the AI's corresponding responses are accurately captured from the web page's DOM.
4.  The captured conversation data is successfully transmitted from the browser extension to the local Python backend service.

### Story 1.4: Persisting Captured Conversations
**As an** AI Power User,
**I want** the conversations captured by the browser extension to be processed and saved into my local memory,
**so that** they are permanently stored and available for future retrieval.

**Acceptance Criteria:**
1.  The Python backend successfully receives the conversation data from the browser extension.
2.  The backend generates vector embeddings from the captured text.
3.  The conversation's metadata (e.g., timestamp, source URL) is saved into the SQLite database.
4.  The conversation text and its corresponding vector embeddings are saved into the ChromaDB collection.