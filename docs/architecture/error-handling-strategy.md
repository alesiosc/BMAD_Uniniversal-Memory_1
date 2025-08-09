# Error Handling Strategy

### Error Flow
The general flow is that the Python backend will catch specific errors and respond with a standardized JSON error format. The React frontend will then parse this response and display a user-friendly message.
```mermaid
sequenceDiagram
    ReactUI->>+PythonBackend: Makes API Request
    PythonBackend->>PythonBackend: Process Request
    alt Error Occurs
        PythonBackend->>PythonBackend: Catch exception, format standard error JSON
        PythonBackend-->>-ReactUI: Respond with HTTP 4xx/5xx and Error JSON
        ReactUI->>ReactUI: Parse error, display user-friendly message
    else Success
        PythonBackend-->>-ReactUI: Respond with HTTP 2xx and Data
    end

    interface ApiError {
  error: {
    code: string; // e.g., "DATABASE_ERROR"
    message: string; // "Could not save the conversation."
    timestamp: string;
    requestId: string;
  };
}

// src/services/apiClient.ts
// ... (inside a request function)
if (!response.ok) {
  const errorPayload = await response.json();
  // Pass this error to a UI notification service
  throw new Error(errorPayload.error.message);
}

# api/src/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class DatabaseError(Exception):
    pass

app = FastAPI()

@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "DATABASE_ERROR",
                "message": "A database error occurred.",
                # ... add timestamp, requestId etc.
            }
        },
    )