from sqlalchemy.orm import Session
from app.db.models import Agent
from app.models.agent import AgentModel, AgentMatch
from typing import List
import numpy as np

class DatabaseService:
    def insert_agent(self, db: Session, agent: AgentModel, embedding: list):
        db_agent = Agent(
            id=agent.id,
            metadata=agent.metadata.dict(),
            embedding=embedding
        )
        db.add(db_agent)
        db.commit()
        return db_agent
        
    def find_similar_agents(self, db: Session, query_embedding: list, top_k: int = 5) -> List[AgentMatch]:
        # Using pgvector's cosine similarity operator (<->)
        similar_agents = db.query(Agent).order_by(
            Agent.embedding.cosine_distance(query_embedding)
        ).limit(top_k).all()
        
        return [
            AgentMatch(
                id=agent.id,
                metadata=agent.metadata,
                similarity_score=1 - self.cosine_distance(query_embedding, agent.embedding)
            )
            for agent in similar_agents
        ]
        
    @staticmethod
    def cosine_distance(a: list, b: list) -> float:
        return 1 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)) 