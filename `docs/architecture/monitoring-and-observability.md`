# Monitoring and Observability

### Monitoring Stack
* **Frontend Monitoring:** The Tauri application will be configured to write logs (including errors from the React UI) to a local file, for example, `~/.universal-memory/logs/frontend.log`.
* **Backend Monitoring:** The Python backend service will use Python's built-in logging module to write logs to a separate local file, `~/.universal-memory/logs/backend.log`.
* **Error Tracking:** No external error tracking service (like Sentry or Datadog) will be used, in adherence with the local-first principle. Errors will be captured exclusively in the local log files.

### Key Metrics
The application will log key events that can be used to manually assess performance and reliability:
* **Frontend Metrics:**
    * Application startup time.
    * Errors encountered in the UI.
    * API response times from the local backend.
* **Backend Metrics:**
    * API request rate and response times.
    * Database query performance (execution time).
    * Errors encountered during conversation processing or database operations.