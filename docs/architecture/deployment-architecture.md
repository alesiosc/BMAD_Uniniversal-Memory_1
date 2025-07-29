# Deployment Architecture

### Deployment Strategy
As a local-first desktop application, "deployment" does not involve cloud servers. Instead, it is the process of building and distributing platform-specific installers for users to download and run on their own machines.

* **Frontend Deployment:** The React UI is not deployed separately. It is bundled directly into the Tauri application.
* **Backend Deployment:** The Python backend is not deployed separately. It is bundled by Tauri as a "sidecar" that is packaged with and managed by the main desktop application.

### CI/CD Pipeline
A Continuous Integration/Continuous Deployment (CI/CD) pipeline will be set up using a tool like GitHub Actions. Its responsibilities will be:
1.  **On every push:** Run linters, unit tests, and integration tests for all parts of the application.
2.  **On a new release tag:** Automatically build the application for all three target platforms (Windows, macOS, Linux), creating `.msi`, `.dmg`, and `.AppImage` installers, and attach them to a new GitHub Release.