# Development Workflow

### Local Development Setup
**Prerequisites**
A developer will need Node.js, npm, and Python installed on their machine.

**Initial Setup**
After cloning the repository, the developer will need to install dependencies for all workspaces.
```bash
# Install all npm dependencies for the desktop app, extension, etc.
npm install

# Install Python dependencies for the backend API
pip install -r apps/api/requirements.txt