# RAG Document Q&A System - Walkthrough

The Retrieval-Augmented Generation (RAG) system is now complete and running! Here is a breakdown of what was built and how to use it.

## 🚀 How to Use It

1. **Open the App:** Navigate to `http://localhost:8501` in your browser. This will open the Streamlit user interface.
2. **Upload Documents:** In the left sidebar, upload one or more PDF files and click **"Process Documents"**.
   - Your documents will be chunked, embedded using `all-mpnet-base-v2`, and stored locally via ChromaDB.
3. **Ask Questions:** In the main chat area, ask questions about your uploaded documents.
   - The system will retrieve relevant context from the PDFs and use Google's `gemini-2.5-flash` model to give a precise, grounded answer. You will also see exactly which pages were cited in the "View Sources" dropdown.

## 🏗️ What Was Built

### 1. Vector Embeddings with SentenceTransformers (Local)
Instead of relying on a paid API, we integrated the local `all-mpnet-base-v2` HuggingFace embedding model. This generates high-quality semantic vectors without extra API costs, stored seamlessly in your local ChromaDB.

### 2. FastAPI Backend
The core application service runs on port `8000` and features:
- `POST /upload`: A high-throughput endpoint to parse PDFs into text, split into 1000-character chunks with overlap, generate embeddings, and store them robustly.
- `POST /query`: Handles the RAG pipeline. It retrieves the top 5 relevant document chunks and securely queries Gemini with strict prompt instructions preventing hallucinations. It returns both the answer and the metadata of the cited sources (e.g., source file name, page number).

### 3. Streamlit Frontend
Served on port `8501`, the interface is intuitive and maintains the entire chat history in session state.

## 🔎 Verification
- The servers are actively running in the background.
- Feel free to test with a document containing facts only known to that document, to verify perfectly grounded generation without hallucination.
