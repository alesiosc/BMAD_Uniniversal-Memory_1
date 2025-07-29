# Core Workflows
This diagram shows the end-to-end sequence for capturing a new conversation and then later searching for it.

```mermaid
sequenceDiagram
    actor User
    participant BrowserExtension
    participant ReactUI
    participant PythonBackend
    participant Databases

    Note over User, BrowserExtension: Conversation Capture
    User->>+BrowserExtension: Interacts with AI on a webpage
    BrowserExtension->>+PythonBackend: POST /conversations (sends captured data)
    PythonBackend->>+Databases: Store metadata (SQLite) & vector (ChromaDB)
    Databases-->>-PythonBackend: Confirm save
    PythonBackend-->>-BrowserExtension: 201 Created
    BrowserExtension-->>-User: (Capture is silent/in background)

    Note over User, ReactUI: Memory Search & Retrieval
    User->>+ReactUI: Opens app and types search query
    ReactUI->>+PythonBackend: POST /search (sends search query)
    PythonBackend->>+Databases: Perform semantic vector search (ChromaDB)
    Databases-->>-PythonBackend: Return relevant results
    PythonBackend-->>-ReactUI: 200 OK (returns search results)
    ReactUI-->>-User: Displays search results