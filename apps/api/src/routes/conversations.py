from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from chromadb import Client as ChromaClient
from typing import List

from ..models.conversation import Conversation as ConversationModel, SearchQuery
from ..db.session import get_db, get_chroma_client
from ..db.repository import ConversationRepository

router = APIRouter()
repo = ConversationRepository()

# (create_conversation, read_conversations, read_conversation, search_conversations endpoints remain the same)

@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    chroma_client: ChromaClient = Depends(get_chroma_client)
):
    """
    Deletes a conversation by its ID.
    """
    deleted_conversation = repo.delete_conversation_by_id(
        db=db, chroma_client=chroma_client, conversation_id=conversation_id
    )
    if deleted_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return