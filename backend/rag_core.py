import os
import logging
import tempfile
from typing import Dict, Any, List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from backend.config import get_settings, validate_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()

embeddings = None
vector_store = None
llm = None


def get_embeddings():
    """Lazy initialization of embeddings model."""
    global embeddings
    if embeddings is None:
        embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    return embeddings


def get_vector_store():
    """Lazy initialization of vector store."""
    global vector_store
    if vector_store is None:
        vector_store = Chroma(
            collection_name="rag_docs",
            embedding_function=get_embeddings(),
            persist_directory=settings.chroma_path
        )
    return vector_store


def get_llm():
    """Lazy initialization of LLM."""
    global llm
    if llm is None:
        validate_settings()
        llm = ChatGoogleGenerativeAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.google_api_key
        )
    return llm

def process_and_add_pdf(file_bytes: bytes, filename: str) -> int:
    logger.info(f"Processing PDF: {filename}")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} pages from {filename}")

        for doc in documents:
            doc.metadata["source_file"] = filename

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Split into {len(chunks)} chunks")
        
        if chunks:
            get_vector_store().add_documents(chunks)
        
        return len(chunks)
    finally:
        os.remove(tmp_path)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def query_rag(question: str) -> Dict[str, Any]:
    logger.info(f"Processing query: {question[:50]}...")
    
    retriever = get_vector_store().as_retriever(search_kwargs={"k": settings.retriever_k})

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, just say that you don't know. "
        "Do not hallucinate or use outside knowledge. "
        "Always cite the source explicitly (using the Source file name and Page number) when providing your answer. "
        "\n\nContext: {context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])
    
    docs = retriever.invoke(question)
    context_str = format_docs(docs)
    
    llm_instance = get_llm()
    chain = prompt | llm_instance | StrOutputParser()
    answer = chain.invoke({"context": context_str, "question": question})
    
    sources = []
    for doc in docs:
        sources.append({
            "content": doc.page_content,
            "metadata": doc.metadata
        })

    return {
        "answer": answer,
        "sources": sources
    }
