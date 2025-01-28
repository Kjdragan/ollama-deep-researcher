# RAG Example

This example demonstrates how to implement a Retrieval-Augmented Generation (RAG) system using Pydantic AI. The system retrieves relevant context from a document collection before generating responses.

## Overview

The example shows how to:
- Create a RAG agent that uses document context for responses
- Implement document retrieval and context selection
- Generate responses using both the query and retrieved context

## Requirements

- PostgreSQL with pgvector extension (can be run via Docker)
- OpenAI API key for embeddings
- Python dependencies: asyncpg, httpx, logfire, pydantic-core, openai

## Setup

1. Start PostgreSQL with pgvector:
```bash
mkdir postgres-data
docker run --rm \
  -e POSTGRES_PASSWORD=postgres \
  -p 54320:5432 \
  -v `pwd`/postgres-data:/var/lib/postgresql/data \
  pgvector/pgvector:pg17
```

2. Build the search database:
```bash
python -m pydantic_ai_examples.rag build
```

3. Run a search query:
```bash
python -m pydantic_ai_examples.rag search "How do I configure logfire to work with FastAPI?"
```

## Implementation Details

The implementation includes:
1. A document retrieval function that finds relevant context using vector similarity search
2. A RAG agent that combines the context with the user's query
3. Response generation using the combined information
4. PostgreSQL with pgvector for efficient vector similarity search

See `rag.py` for the complete implementation.