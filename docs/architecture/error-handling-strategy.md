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