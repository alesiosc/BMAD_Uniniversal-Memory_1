# API Specification

### REST API Specification
This OpenAPI specification outlines the core endpoints for managing conversations. The server will run locally, managed by the Tauri application.

```yaml
openapi: 3.0.0
info:
  title: Universal Memory Local API
  version: 1.0.0
  description: API for managing and searching local AI conversation memories.
servers:
  - url: [http://127.0.0.1:8000](http://127.0.0.1:8000)
    description: Local Development Server

paths:
  /conversations:
    post:
      summary: Add a new conversation
      description: Endpoint for the browser extension to submit a newly captured conversation.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Conversation'
      responses:
        '201':
          description: Conversation successfully created.
    get:
      summary: Get all conversations
      description: Retrieves a paginated list of all conversation metadata from SQLite.
      responses:
        '200':
          description: A list of conversations.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Conversation'

  /conversations/{id}:
    get:
      summary: Get a single conversation
      description: Retrieves the full details of a single conversation.
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: The full conversation.
    delete:
      summary: Delete a conversation
      description: Deletes a conversation from both SQLite and ChromaDB.
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Conversation successfully deleted.

  /search:
    post:
      summary: Search conversations
      description: Performs a semantic vector search across all stored conversations.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
      responses:
        '200':
          description: A list of relevant conversation results, ranked by similarity.

components:
  schemas:
    ConversationTurn:
      type: object
      properties:
        speaker:
          type: string
          enum: [user, ai]
        text:
          type: string
    Conversation:
      type: object
      properties:
        id:
          type: string
          format: uuid
        source:
          type: string
        timestamp:
          type: number
        content:
          type: array
          items:
            $ref: '#/components/schemas/ConversationTurn'