from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from chromadb import Client as ChromaClient
from typing import List

# FIX: Changed the model import to be relative (from .models -> from ..models)
from ..models.conversation import Conversation as ConversationModel, SearchQuery, SearchResult

from ..db.session import get_db, get_chroma_client
from ..db.repository import ConversationRepository

router = APIRouter()
repo = ConversationRepository()

# ... (all other routes will be added in later stories)

@router.get("/conversations", response_model=List[ConversationModel])
async def read_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all conversation metadata.
    """
    conversations = repo.get_all_conversations(db=db, skip=skip, limit=limit)
    return conversations