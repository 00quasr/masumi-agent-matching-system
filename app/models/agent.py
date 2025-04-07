from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel

class AgentMetadata(BaseModel):
    name: str
    description: str
    capabilities: List[str]
    agent_type: str
    dependencies: List[str]

class AgentModel(BaseModel):
    id: UUID
    metadata: AgentMetadata

class AgentMatch(BaseModel):
    id: UUID
    metadata: AgentMetadata
    similarity_score: float 