# RAG Document Q&A System

A production-ready Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents and ask questions to get cited, grounded answers using local embeddings and Google Gemini LLM.

## Features

- **PDF Upload**: Support for multiple PDF file uploads
- **Semantic Search**: Local embeddings using sentence-transformers
- **Grounded Answers**: Google Gemini 2.0 Flash for accurate, cited responses
- **Source Attribution**: Every answer includes source document and page references
- **RESTful API**: FastAPI backend with health check endpoints
- **Interactive UI**: Streamlit chat interface
- **Production Ready**: Logging, error handling, configuration management

## Architecture

```
rag_qa_system/
├── backend/
│   ├── main.py          # FastAPI endpoints
│   ├── rag_core.py      # RAG logic
│   └── config.py        # Configuration
├── frontend/
│   └── app.py           # Streamlit UI
├── tests/               # Unit tests
└── chroma_db/          # Vector store
```

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
cd rag_qa_system

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Or (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google API key
# Get one at: https://aistudio.google.com/app/apikey
```

### 3. Run the Application

```bash
# Terminal 1: Start backend
uvicorn backend.main:app --reload

# Terminal 2: Start frontend
streamlit run frontend/app.py
```

### 4. Use the App

- Open http://localhost:8501 in your browser
- Upload PDF documents in the sidebar
- Ask questions about your documents
- View source citations in the expander

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/upload` | POST | Upload PDF |
| `/query` | POST | Ask a question |

### Example Usage

```bash
# Upload a PDF
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"

# Ask a question
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

## Configuration

All settings are managed via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | (required) | Google Gemini API key |
| `EMBEDDING_MODEL` | all-mpnet-base-v2 | HuggingFace model |
| `LLM_MODEL` | gemini-2.0-flash | Gemini model |
| `LLM_TEMPERATURE` | 0.0 | LLM temperature |
| `CHUNK_SIZE` | 1000 | Text chunk size |
| `CHUNK_OVERLAP` | 200 | Chunk overlap |
| `RETRIEVER_K` | 5 | Top-K results |

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend tests/

# Run specific test file
pytest tests/test_api.py -v
```

## Technology Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **RAG**: LangChain, LangChain-Google-GenAI
- **Embeddings**: sentence-transformers
- **Vector Store**: ChromaDB
- **LLM**: Google Gemini 2.0 Flash
- **Testing**: pytest, httpx

## Production Considerations

For production deployment, consider:

1. **CORS**: Restrict `allow_origins` in `main.py`
2. **Authentication**: Add user auth (OAuth2/JWT)
3. **Rate Limiting**: Add slowapi middleware
4. **HTTPS**: Use TLS/SSL
5. **Docker**: Add Dockerfile and docker-compose.yml
6. **Monitoring**: Add Prometheus metrics

## License

MIT
