#!/bin/bash

echo "Starting RAG Q&A System..."

echo "Starting backend on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

sleep 3

echo "Starting frontend on port 8501..."
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0

wait
