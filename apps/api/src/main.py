from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from .db.session import create_db_and_tables
from .core.config import settings
from .routes import conversations

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    print("Initializing database...")
    create_db_and_tables()
    print("Database initialization complete.")

    print("Loading embedding model...")
    app.state.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    print("Embedding model loaded.")

    yield
    # On shutdown
    print("Application shutting down.")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # The origin of your Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversations.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}