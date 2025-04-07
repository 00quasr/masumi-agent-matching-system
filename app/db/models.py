from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
from .database import Base

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metadata = Column(JSON, nullable=False)
    embedding = Column(Vector(384))  # MiniLM-L6-v2 dimension 