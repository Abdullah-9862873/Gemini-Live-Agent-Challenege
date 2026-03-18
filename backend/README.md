---
title: Making Repos Speakable
emoji: 🗣️
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: "3.10"
app_file: main.py
python_version: "3.10"
pinned: false
---

# Making Repos Speakable

**Give brain and tongue to your GitHub repositories.**

An AI-powered application that transforms GitHub repositories into interactive, queryable knowledge bases using RAG (Retrieval-Augmented Generation) and Groq LLM.

## Features

- GitHub repository validation and ingestion
- RAG-powered Q&A with vector search
- Single file upload support
- Voice output with Text-to-Speech
- Groq LLM integration (free, no billing)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/validate-repo` | Validate GitHub repository |
| POST | `/ingest` | Ingest repository |
| GET | `/ingest/status` | Get ingestion status |
| POST | `/ingest/clear` | Clear all vectors |
| POST | `/ingest/single` | Upload single file |
| POST | `/ask` | Ask a question |
| POST | `/ask/single` | Ask about uploaded file |

## Environment Variables (Set in Space Secrets)

- `GROQ_API_KEY` - Groq API key (get free at https://console.groq.com/)
- `PINECONE_API_KEY` - Pinecone API key
- `PINECONE_INDEX_NAME` - Pinecone index name (e.g., `making-repos-speakable`)
- `GITHUB_TOKEN` - GitHub token for private repos (optional)

## License

MIT
