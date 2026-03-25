# AGENTS.md - Agentic Coding Guidelines for rag_qa_system

This file provides guidance for AI coding agents working in this repository.

## Project Overview

RAG-powered document Q&A system with FastAPI backend and Streamlit frontend. Users upload PDFs and ask questions to get cited, grounded answers using local embeddings and Google Gemini LLM.

## Build / Run Commands

### Environment Setup
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Unix/Linux

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start FastAPI backend (port 8000)
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# Start Streamlit frontend (port 8501) - in separate terminal
streamlit run frontend/app.py
```

### Testing
```bash
# Install pytest for testing (not currently in requirements)
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run a single test file
pytest tests/test_rag_core.py

# Run a single test function
pytest tests/test_rag_core.py::test_process_pdf

# Run tests with verbose output
pytest -v

# Run tests matching a pattern
pytest -k "test_query"
```

### Linting / Type Checking
```bash
# Install linting tools
pip install ruff black mypy

# Run ruff linter
ruff check .

# Auto-fix with ruff
ruff check . --fix

# Format code with black
black .

# Type checking with mypy
mypy .
```

## Code Style Guidelines

### Imports
- Use absolute imports within the project: `from backend.rag_core import ...`
- Order imports: standard library, third-party, local application
- Group by type: exceptions, classes, functions
- Use explicit imports rather than wildcard (`from x import *`)

### Formatting
- Line length: 88 characters (Black default)
- Use 4 spaces for indentation (not tabs)
- Use trailing commas in multi-line structures
- Add spaces around operators and after commas

### Type Hints
- Use type hints for all function parameters and return types
- Use `Optional[X]` instead of `X | None` for compatibility
- Use `Dict`, `List`, `Tuple` from typing module
- Example: `def process_and_add_pdf(file_bytes: bytes, filename: str) -> int:`

### Naming Conventions
- Variables/functions: `snake_case` (e.g., `file_bytes`, `process_and_add_pdf`)
- Classes: `PascalCase` (e.g., `QueryRequest`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `CHROMA_PATH`)
- Private functions: prefix with underscore (e.g., `_format_docs`)

### Error Handling
- Use specific exception types rather than bare `except:`
- Raise `HTTPException` for API errors with appropriate status codes
- Validate inputs at API boundaries (e.g., file type checking in `/upload`)
- Return meaningful error messages: `detail="Only PDF files are supported."`

### API Design
- Use FastAPI decorators for HTTP methods: `@app.post()`, `@app.get()`
- Define request/response models using Pydantic `BaseModel`
- Use async/await for I/O-bound operations
- Add docstrings to endpoint functions

### Async Patterns
- Mark file upload handlers as `async`
- Use `await` for async library calls
- Keep async functions non-blocking

## Project Structure

```
rag_qa_system/
├── backend/
│   ├── main.py          # FastAPI app, endpoints: /upload, /query
│   └── rag_core.py      # RAG logic: PDF processing, embeddings, ChromaDB
├── frontend/
│   └── app.py           # Streamlit UI with chat interface
├── chroma_db/           # Persistent vector store
├── requirements.txt
├── CLAUDE.md            # Original Claude Code guidance
└── AGENTS.md            # This file
```

## Key Technical Details

- **Embedding Model**: `sentence-transformers/all-mpnet-base-v2` (local)
- **LLM**: Google `gemini-2.5-flash` with temperature 0.0
- **Vector Store**: ChromaDB with persistent storage at `./chroma_db`
- **Chunking**: RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
- **API Key**: Uses environment variable `GOOGLE_API_KEY` (see `.env.example`)

## Database / State

- ChromaDB persists vector embeddings to `./chroma_db/` directory
- No migration system needed (ChromaDB handles persistence automatically)
- To reset: delete the `chroma_db/` folder

## Security Notes

- File validation: Only PDF files accepted (`.endswith(".pdf")`)
- CORS configured to allow all origins (`allow_origins=["*"]`)
- API key is hardcoded - should be moved to environment variable for production

## Testing Strategy

Since this project has no tests yet, agents should:
1. Add `pytest` and `pytest-asyncio` to `requirements.txt`
2. Create `tests/` directory with test files
3. Test RAG functions in isolation (mock ChromaDB/Gemini if needed)
4. Use FastAPI's `TestClient` for endpoint testing

## Cursor / Copilot Rules

No `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md` files exist in this project.
