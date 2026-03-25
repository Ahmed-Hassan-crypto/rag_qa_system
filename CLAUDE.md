# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix/Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the FastAPI backend (port 8000)
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# Start the Streamlit frontend (port 8501)
streamlit run frontend/app.py

# Or start both services manually in separate terminals
```

### Testing
```bash
# Test backend health
curl http://127.0.0.1:8000/docs  # FastAPI interactive docs

# Test document upload (example)
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@document.pdf"

# Test querying
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic of the document?"}'
```

## Code Architecture

### High-Level Structure
```
rag_qa_system/
├── backend/              # FastAPI service (port 8000)
│   ├── main.py          # API endpoints: /upload, /query
│   └── rag_core.py      # RAG logic: PDF processing, embeddings, querying
├── frontend/            # Streamlit UI (port 8501)
│   └── app.py           # File upload, chat interface, source display
├── chroma_db/           # Persistent vector store (auto-generated)
├── requirements.txt     # Python dependencies
├── implementation_plan.md  # Detailed architecture and setup guide
└── walkthrough.md       # Usage instructions
```

### Component Responsibilities

**Backend (FastAPI):**
- `main.py`: REST API with CORS middleware
  - POST `/upload`: Accepts PDF files, validates format, delegates processing
  - POST `/query`: Accepts questions, returns answers with source citations
- `rag_core.py`: Core RAG implementation
  - PDF text extraction using PyPDFLoader
  - Text chunking with RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
  - Local embeddings via HuggingFace `all-mpnet-base-v2` model
  - Vector storage in ChromaDB (persistent at `./chroma_db`)
  - Grounded Q&A using Google Gemini 2.5 Flash with anti-hallucination prompts
  - Source attribution with filename and page number metadata

**Frontend (Streamlit):**
- `app.py`: Interactive chat interface
  - Sidebar for multi-file PDF upload with processing status
  - Main chat area with message history
  - Source expansion panels showing cited document chunks
  - Session state management for chat persistence
  - HTTP client communicating with backend at `http://127.0.0.1:8000`

### Data Flow
1. User uploads PDF via Streamlit frontend → POST to `/upload` endpoint
2. Backend saves temp file, extracts text, chunks content, adds metadata
3. Embeddings generated locally, stored in ChromaDB with source/page metadata
4. User asks question via chat interface → POST to `/query` endpoint
5. Backend retrieves top-5 relevant chunks, constructs grounded prompt
6. Gemini 2.5 Flash generates answer with explicit source citations
7. Frontend displays answer with expandable source references

### Key Technical Details
- Embedding Model: `sentence-transformers/all-mpnet-base-v2` (local, no API cost)
- LLM: Google `gemini-2.5-flash` (temperature 0.0 for deterministic outputs)
- Vector Store: ChromaDB with persistent storage at `./chroma_db`
- Chunking Strategy: Recursive character splitting with overlap for context preservation
- Security: File type validation (PDF-only), CORS configured for development
- Prompt Engineering: Strict anti-hallucination instructions forcing citations