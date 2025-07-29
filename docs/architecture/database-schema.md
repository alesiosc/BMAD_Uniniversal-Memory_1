# Database Schema

### SQLite Schema
This schema defines the table for storing the core metadata of each captured conversation. It is designed to be lightweight and fast for fetching lists of memories.

```sql
CREATE TABLE conversations (
    id TEXT PRIMARY KEY NOT NULL,
    source TEXT NOT NULL,
    timestamp INTEGER NOT NULL
);

CREATE INDEX idx_conversations_timestamp ON conversations (timestamp);