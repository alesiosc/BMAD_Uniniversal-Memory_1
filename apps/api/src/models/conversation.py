from pydantic import BaseModel
from typing import List

class ConversationTurn(BaseModel):
    speaker: str
    text: str

class Conversation(BaseModel):
    id: str | None = None
    source: str
    timestamp: int
    content: List[ConversationTurn]

class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    id: str
    source: str
    timestamp: int
    snippet: str