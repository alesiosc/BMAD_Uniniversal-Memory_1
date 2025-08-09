# Unified Project Structure
This structure uses `npm workspaces` and organizes each major part of the application into its own package.

```plaintext
universal-memory/
├── apps/
│   ├── desktop/              # Tauri/React Frontend App
│   │   ├── src/
│   │   ├── src-tauri/
│   │   └── package.json
│   ├── extension/            # Browser Extension
│   │   ├── src/
│   │   └── manifest.json
│   └── api/                  # Python Backend (FastAPI)
│       └── src/
├── packages/
│   ├── shared-types/         # Shared TypeScript interfaces
│   │   └── index.ts
│   └── ui/                   # Shared React UI components (optional)
├── .gitignore
└── package.json              # Root package.json with workspaces config