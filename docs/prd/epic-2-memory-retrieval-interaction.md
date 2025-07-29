# Epic 2: Memory Retrieval & Interaction

**Goal:** This epic builds upon the foundation of Epic 1. Now that conversations are being captured, the focus shifts to making that data useful. By the end of this epic, the user will have a functional desktop dashboard where they can view, semantically search, and manage all their captured memories, effectively transforming the collected raw data into an accessible and interactive "external brain".

### Story 2.1: Dashboard Memory Feed
**As an** AI Power User,
**I want** to see a list of my most recent memories in the dashboard,
**so that** I can quickly review what has been captured.

**Acceptance Criteria:**
1.  The main screen of the Tauri desktop application displays a list of captured conversations.
2.  The list is sorted in reverse chronological order, with the newest memories appearing first.
3.  Each item in the list displays a short preview (e.g., the first line of the prompt), the source (e.g., website name), and the capture timestamp.
4.  The application successfully fetches and displays this data from the local SQLite database.

### Story 2.2: View Full Conversation Detail
**As an** AI Power User,
**I want** to select a memory from the dashboard list and view the full conversation,
**so that** I can read the entire interaction in detail.

**Acceptance Criteria:**
1.  Clicking on a memory item in the main feed navigates the user to a dedicated "detail view".
2.  The detail view renders the entire content of the selected conversation.
3.  The display clearly distinguishes between the user's prompts and the AI's responses.
4.  The relevant metadata for the conversation (source, full timestamp, etc.) is also displayed.

### Story 2.3: Semantic Memory Search
**As an** AI Power User,
**I want** to perform a semantic search across all my memories using a simple search bar,
**so that** I can find relevant context even if I don't remember the exact keywords.

**Acceptance Criteria:**
1.  The dashboard UI includes a prominent and accessible search input field.
2.  When a user submits a query, the Python backend generates a vector embedding for the query text.
3.  A vector search is performed against the ChromaDB collection to find the most relevant saved conversations.
4.  A list of search results, ranked by relevance, is displayed to the user in the UI.

### Story 2.4: Manual Memory Management
**As an** AI Power User,
**I want** to manually import and delete conversations from the dashboard,
**so that** I have full control over the contents of my memory.

**Acceptance Criteria:**
1.  The dashboard provides a UI option to import a conversation from a supported format (e.g., a plain text file).
2.  The dashboard provides a clear and accessible option to delete a selected conversation.
3.  The user is shown a confirmation prompt before a memory is permanently deleted.
4.  A successful deletion removes the memory's metadata from SQLite and its vector data from ChromaDB.