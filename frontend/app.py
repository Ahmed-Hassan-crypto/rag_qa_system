import streamlit as st
import requests
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="RAG Document Q&A", page_icon="📚", layout="wide")

st.title("📚 RAG-Powered Document Q&A System")
st.markdown("Upload PDFs and ask questions to get cited, grounded answers.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📄 Document Upload")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Process Documents"):
        if uploaded_files:
            with st.spinner("Processing documents..."):
                for uploaded_file in uploaded_files:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    try:
                        response = requests.post(f"{BACKEND_URL}/upload", files=files)
                        if response.status_code == 200:
                            st.success(f"Processed: {uploaded_file.name}")
                        else:
                            st.error(f"Failed to process {uploaded_file.name}: {response.text}")
                    except Exception as e:
                        st.error(f"Error connecting to backend: {e}")
        else:
            st.warning("Please upload files first.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("View Sources"):
                for i, source in enumerate(message["sources"]):
                    st.markdown(f"**Source {i+1}:** {source['metadata'].get('source_file', 'Unknown')} (Page {source['metadata'].get('page', 'Unknown')})")
                    st.caption(source["content"])

if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{BACKEND_URL}/query", json={"question": prompt})
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])
                    
                    st.markdown(answer)
                    
                    if sources:
                        with st.expander("View Sources"):
                            for i, source in enumerate(sources):
                                meta = source.get("metadata", {})
                                st.markdown(f"**Source {i+1}:** {meta.get('source_file', 'Unknown')} (Page {meta.get('page', 'Unknown')})")
                                st.caption(source.get("content", ""))
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources
                    })
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
