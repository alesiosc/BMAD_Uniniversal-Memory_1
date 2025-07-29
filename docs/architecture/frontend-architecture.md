# Frontend Architecture

### Component Architecture
**Component Organization**
We will organize components into a clear hierarchy within the `src/components` directory to distinguish between generic, reusable elements and feature-specific ones.
```text
src/
└── components/
    ├── ui/
    │   ├── Button.tsx
    │   └── SearchBar.tsx
    ├── layout/
    │   ├── Sidebar.tsx
    │   └── PageWrapper.tsx
    └── features/
        ├── MemoryFeed.tsx
        └── ConversationView.tsx