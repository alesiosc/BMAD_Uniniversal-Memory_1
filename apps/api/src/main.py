from fastapi import FastAPI
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

app.include_router(conversations.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}