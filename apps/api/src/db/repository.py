import uuid
import json
from sqlalchemy.orm import Session
from sqlalchemy import desc
from chromadb import Client as ChromaClient
from ..models.conversation import Conversation as ConversationModel
from .session import Conversation as ConversationSchema

class ConversationRepository:
    def _concatenate_content(self, conversation: ConversationModel) -> str:
        return "\n".join([f"{turn.speaker}: {turn.text}" for turn in conversation.content])

    def add_conversation(self, db: Session, chroma_client: ChromaClient, conversation: ConversationModel, model):
        conversation_id = str(uuid.uuid4())
        db_conversation = ConversationSchema(
            id=conversation_id,
            source=conversation.source,
            timestamp=conversation.timestamp
        )
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)

        full_text = self._concatenate_content(conversation)
        embedding = model.encode(full_text).tolist()
        
        content_dict = [turn.dict() for turn in conversation.content]
        
        collection = chroma_client.get_or_create_collection(name="conversations")
        collection.add(
            ids=[conversation_id],
            embeddings=[embedding],
            documents=[full_text],
            metadatas=[{"source": conversation.source, "timestamp": conversation.timestamp, "content": json.dumps(content_dict)}]
        )
        return db_conversation

    def get_all_conversations(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(ConversationSchema).order_by(desc(ConversationSchema.timestamp)).offset(skip).limit(limit).all()

    def get_conversation_by_id(self, db: Session, chroma_client: ChromaClient, conversation_id: str):
        db_conversation = db.query(ConversationSchema).filter(ConversationSchema.id == conversation_id).first()
        if not db_conversation:
            return None

        collection = chroma_client.get_or_create_collection(name="conversations")
        chroma_result = collection.get(ids=[conversation_id], include=["metadatas"])
        
        if not chroma_result or not chroma_result['ids']:
            return None

        metadata = chroma_result['metadatas'][0]
        content_json = metadata.get("content", "[]")
        
        return {
            "id": db_conversation.id,
            "source": db_conversation.source,
            "timestamp": db_conversation.timestamp,
            "content": json.loads(content_json)
        }

    def search_conversations(self, chroma_client: ChromaClient, query: str, model, top_k: int = 5):
        collection = chroma_client.get_or_create_collection(name="conversations")
        query_embedding = model.encode(query).tolist()
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["metadatas", "documents"] 
        )
        
        search_results = []
        if results and results['ids'][0]:
            for i, result_id in enumerate(results['ids'][0]):
                meta = results['metadatas'][0][i]
                document = results['documents'][0][i]
                search_results.append({
                    "id": result_id,
                    "source": meta.get("source"),
                    "timestamp": meta.get("timestamp"),
                    "snippet": document[:200] + "..." if len(document) > 200 else document
                })
        
        return search_results

    def delete_conversation_by_id(self, db: Session, chroma_client: ChromaClient, conversation_id: str):
        db_conversation = db.query(ConversationSchema).filter(ConversationSchema.id == conversation_id).first()
        if not db_conversation:
            return None

        db.delete(db_conversation)
        db.commit()

        collection = chroma_client.get_or_create_collection(name="conversations")
        collection.delete(ids=[conversation_id])

        return db_conversation