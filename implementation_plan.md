# RAG-Powered Document Q&A System Implementation Plan

This project implements a Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents and ask questions about them. The system will extract text, chunk it, embed it using the local `all-mpnet-base-v2` model through `SentenceTransformers`, store it in ChromaDB, and use Google's `gemini-2.5-flash` to answer questions with citations to avoid hallucinations.

## Proposed Changes

### Environment
We will create a Python virtual environment (`.venv`) inside the project folder to isolate dependencies and store the libraries.

### Architecture
We will create a multi-service architecture within a single workspace:
- **Backend (FastAPI)**: Handles document ingestion, vector searches, and LLM communication.
- **Frontend (Streamlit)**: Provides a user-friendly UI for uploading PDFs and asking questions.

### Project Structure (Workspace: `C:\2026 AI Projects\rag_qa_system`)

#### [NEW] `requirements.txt`
Dependencies including `fastapi`, `uvicorn`, `streamlit`, `langchain`, `langchain-google-genai`, `langchain-huggingface`, `sentence-transformers`, `chromadb`, `pypdf`, `python-multipart`.

#### [NEW] `backend/main.py`
FastAPI application with two main endpoints:
- `POST /upload`: Accepts PDF files, processes them, and stores embeddings in ChromaDB.
- `POST /query`: Accepts a question, retrieves relevant chunks from ChromaDB, constructs a prompt forcing grounded answers, and calls Gemini to get the response.

#### [NEW] `backend/rag_core.py`
Core RAG logic using LangChain to:
- Parse PDFs and split them into recursive character chunks with metadata (source, page).
- Generate embeddings via `HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")` and store them in a persistent ChromaDB collection.
- Perform similarity search given a query.
- Call `gemini-2.5-flash` with a strict system prompt to prevent hallucinations and strictly cite sources using the metadata.

#### [NEW] `frontend/app.py`
Streamlit application that:
- Maintains session state for uploaded documents and chat history.
- Provides a sidebar for uploading multiple PDF files to the FastAPI backend.
- Provides a chat interface where the user can ask questions.
- Displays the LLM's answer along with foldable "Sources" sections to show exactly which document chunks were cited.

## Verification Plan

### Manual Verification
1. Create a Python virtual environment and install dependencies via `pip install -r requirements.txt`.
2. Start the FastAPI backend server on port 8000 using the virtual environment.
3. Start the Streamlit frontend server on port 8501 using the virtual environment.
4. Open the Streamlit UI, upload sample PDFs.
5. Ask queries that are explicitly covered in the PDFs. Verify correct answers and citations (doc name and page number).
6. Ask a query completely unrelated to the PDFs to verify it refuses to answer.
