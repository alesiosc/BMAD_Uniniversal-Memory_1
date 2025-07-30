import os
import chromadb
from sqlalchemy import create_engine, Column, Integer, String, Index
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Define a local directory for storing database files
APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".universal-memory")
if not os.path.exists(APP_DATA_DIR):
    os.makedirs(APP_DATA_DIR)

# SQLite Configuration
SQLITE_DB_PATH = os.path.join(APP_DATA_DIR, "memory.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modern SQLAlchemy 2.0 Base class
class Base(DeclarativeBase):
    pass

# Define the Conversation model for SQLAlchemy
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True, index=True)
    source = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)

    __table_args__ = (Index('idx_conversations_timestamp', 'timestamp'),)

# ChromaDB Configuration
chroma_client = chromadb.PersistentClient(path=os.path.join(APP_DATA_DIR, "chroma_db"))

def create_db_and_tables():
    """
    Creates the database and tables if they don't already exist.
    Initializes the ChromaDB collection if it doesn't exist.
    """
    Base.metadata.create_all(bind=engine)
    chroma_client.get_or_create_collection(name="conversations")

def get_db():
    """Dependency to get a SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_chroma_client():
    """Dependency to get a ChromaDB client."""
    return chroma_client