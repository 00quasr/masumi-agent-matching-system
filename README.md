# Masumi Agent Matching System

A high-performance semantic matching system for Masumi Agents that helps identify and retrieve similar agents based on their MIP-002 metadata.

## Overview

This system uses semantic embeddings to index and search for agents with similar capabilities, dependencies, and use cases. By vectorizing agent metadata, the system can efficiently find the most relevant agents based on cosine similarity - even when there's no direct keyword match.

## Technical Architecture

The matching system consists of the following components:

- **FastAPI Backend**: REST API endpoints for agent registration and matching
- **Embeddings Engine**: Converts agent metadata to vector representations
- **Vector Database**: Stores embeddings and enables fast similarity search
- **PostgreSQL + pgvector**: Provides vector similarity operations

## Directory Structure

matching-algo/
│
├── app/ # Main application package
│ ├── api/ # API endpoints
│ │ └── endpoints.py # REST API endpoint definitions
│ │
│ ├── core/ # Core configuration
│ │ └── config.py # Application settings
│ │
│ ├── db/ # Database components
│ │ ├── database.py # Database connection setup
│ │ └── models.py # SQLAlchemy models
│ │
│ ├── models/ # Pydantic data models
│ │ └── agent.py # Agent data structures
│ │
│ ├── services/ # Business logic services
│ │ ├── db_service.py # Database operations
│ │ └── embedding_service.py # Vector embedding logic
│ │
│ └── main.py # Application entry point
│
├── .env # Environment variables
└── requirements.txt # Python dependencies

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 14+ with pgvector extension
- 2GB+ RAM (for embedding model)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/matching-algo.git
   cd matching-algo
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL with pgvector:
   ```sql
   CREATE EXTENSION vector;
   CREATE DATABASE masumi;
   ```

5. Configure environment variables in `.env`:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/masumi
   ```

6. Initialize the database:
   ```bash
   python -m app.main
   ```

## How It Works

### Agent Registration

When a new agent is registered, the system:

1. Extracts the agent's MIP-002 metadata (name, description, capabilities, etc.)
2. Formats the metadata into a standardized text representation
3. Generates a 384-dimensional embedding vector using the SentenceTransformer model
4. Stores both the metadata and embedding in the PostgreSQL database

### Agent Matching

When matching agents:

1. The query agent's metadata is converted to the same vector space
2. The system performs a cosine similarity search against all stored agent embeddings
3. The top N most similar agents are returned, ranked by similarity score

### Key Files Explained

#### `app/api/endpoints.py`

Contains the FastAPI route handlers for:
- `/register-agent`: Stores a new agent with its metadata and embedding
- `/match-agent`: Finds similar agents based on provided metadata

#### `app/core/config.py`

Manages application configuration including:
- Database connection string
- Embedding model name and dimensions
- Environment variable management

#### `app/db/database.py`

Handles database connection using SQLAlchemy, including:
- Connection pool setup
- Session management
- Base model definition

#### `app/db/models.py`

Defines the database schema using SQLAlchemy:
- `Agent` table with UUID, JSON metadata, and vector embedding

#### `app/models/agent.py`

Pydantic models for data validation:
- `AgentMetadata`: Structured representation of MIP-002 metadata
- `AgentModel`: Complete agent with ID and metadata
- `AgentMatch`: Agent with added similarity score for query results

#### `app/services/db_service.py`

Database operations:
- Agent insertion
- Similarity search using pgvector
- Cosine distance calculation

#### `app/services/embedding_service.py`

Vector embedding generation:
- Metadata text formatting
- SentenceTransformer model initialization
- Vector conversion and normalization

#### `app/main.py`

Application startup:
- FastAPI app initialization
- Database schema creation
- API router registration

## API Reference

### Register Agent

Register a new agent in the matching system.

POST /api/v1/register-agent

Request body:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "metadata": {
    "name": "SEO Optimizer Agent",
    "description": "Analyzes website structure and improves SEO rankings.",
    "capabilities": ["SEO analysis", "keyword research"],
    "agent_type": "analyzer",
    "dependencies": ["Scraper", "Google Search API"]
  }
}
```

Response:
```json
{
  "message": "Agent registered successfully",
  "agent_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Match Agent

Find similar agents to a provided agent metadata.

POST /api/v1/match-agent

Request body:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "metadata": {
    "name": "SEO Analyzer",
    "description": "Evaluates website content for search engine optimization.",
    "capabilities": ["content analysis", "keyword extraction"],
    "agent_type": "analyzer",
    "dependencies": ["Web Scraper"]
  }
}
```

Query parameters:
- `top_k`: Number of results to return (default: 5)

Response:
```json
[
  {
    "id": "662f9401-a28c-42d3-b716-446655441111",
    "metadata": {
      "name": "Content Optimizer",
      "description": "Improves website content for SEO.",
      "capabilities": ["keyword research", "content analysis"],
      "agent_type": "optimizer",
      "dependencies": ["NLP Engine", "Scraper"]
    },
    "similarity_score": 0.89
  },
  ...
]
```

## Technical Implementation Details

### Vector Generation

The system uses the `all-MiniLM-L6-v2` model from the Sentence Transformers library to create dense vector embeddings. This model:

- Produces 384-dimensional embeddings
- Balances performance and computational efficiency
- Works well with short to medium-length text descriptions

### Similarity Calculation

Similarity between agents is calculated using cosine similarity:

```
similarity = cos(θ) = (A·B)/(||A||·||B||)
```

Where:
- A and B are the embedding vectors
- A·B is the dot product
- ||A|| and ||B|| are the vector magnitudes

### Database Schema

The `agents` table has the following structure:

| Column    | Type            | Description                        |
|-----------|-----------------|----------------------------------- |
| id        | UUID            | Primary key, unique agent ID       |
| metadata  | JSONB           | MIP-002 agent metadata             |
| embedding | vector(384)     | Vector representation of metadata  |

## Development

### Adding New Capabilities

To extend the matching algorithm:

1. Update `app/models/agent.py` to add new metadata fields
2. Modify `app/services/embedding_service.py` to incorporate new fields in the embedding generation
3. Test similarity results with the new fields

### Testing

Run tests with pytest:
```bash
pytest
```

## Performance Considerations

- The SentenceTransformer model loads ~90MB into memory
- Embedding generation takes approximately 50-100ms per agent on CPU
- Vector similarity search scales with O(n) where n is the number of agents
- Consider batch processing for large numbers of agents

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This system follows the MIP-002 specification for Masumi Agent metadata.


