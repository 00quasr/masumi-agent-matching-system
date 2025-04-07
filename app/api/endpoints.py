from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.agent import AgentModel, AgentMatch
from app.services.embedding_service import EmbeddingService
from app.services.db_service import DatabaseService
from app.db.database import get_db
from typing import List

router = APIRouter()
embedding_service = EmbeddingService()
db_service = DatabaseService()

@router.post("/register-agent")
def register_agent(
    agent: AgentModel,
    db: Session = Depends(get_db)
):
    try:
        embedding = embedding_service.generate_embedding(agent.metadata)
        db_service.insert_agent(db, agent, embedding)
        return {"message": "Agent registered successfully", "agent_id": agent.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/match-agent")
def match_agent(
    agent: AgentModel,
    top_k: int = 5,
    db: Session = Depends(get_db)
) -> List[AgentMatch]:
    try:
        query_embedding = embedding_service.generate_embedding(agent.metadata)
        matches = db_service.find_similar_agents(db, query_embedding, top_k)
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 