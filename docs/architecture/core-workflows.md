`# Core Workflows
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
    ReactUI-->>-User: Displays search results`

`---
### **File 25 of 68: Architecture - Database Schema**

**File:** `docs/architecture/database-schema.md`
```markdown
# Database Schema

### SQLite Schema
This schema defines the table for storing the core metadata of each captured conversation. It is designed to be lightweight and fast for fetching lists of memories.

```sql
CREATE TABLE conversations (
    id TEXT PRIMARY KEY NOT NULL,
    source TEXT NOT NULL,
    timestamp INTEGER NOT NULL
);

CREATE INDEX idx_conversations_timestamp ON conversations (timestamp);`