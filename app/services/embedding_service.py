from sentence_transformers import SentenceTransformer
from app.models.agent import AgentMetadata

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def format_metadata(self, metadata: AgentMetadata) -> str:
        return f"""
        Name: {metadata.name}
        Description: {metadata.description}
        Capabilities: {', '.join(metadata.capabilities)}
        Type: {metadata.agent_type}
        Dependencies: {', '.join(metadata.dependencies)}
        """
        
    def generate_embedding(self, metadata: AgentMetadata) -> list:
        text = self.format_metadata(metadata)
        return self.model.encode(text, convert_to_tensor=False).tolist() 