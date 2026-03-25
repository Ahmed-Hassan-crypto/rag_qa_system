import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


os.environ["GOOGLE_API_KEY"] = "test_api_key"


@pytest.fixture(autouse=True)
def setup_env():
    """Set up environment variables for all tests."""
    env = {
        "GOOGLE_API_KEY": "test_api_key",
        "EMBEDDING_MODEL": "all-mpnet-base-v2",
        "LLM_MODEL": "gemini-2.0-flash",
        "LLM_TEMPERATURE": "0.0",
        "CHUNK_SIZE": "1000",
        "CHUNK_OVERLAP": "200",
        "RETRIEVER_K": "5",
        "DEBUG": "false",
    }
    with patch.dict(os.environ, env, clear=True):
        from backend.config import get_settings
        get_settings.cache_clear()
        yield


@pytest.fixture
def client(setup_env):
    """Create test client with mocked dependencies."""
    from backend import main
    return TestClient(main.app)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_200(self, client):
        """Test that health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_format(self, client):
        """Test health endpoint response format."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert data["status"] == "healthy"


class TestUploadEndpoint:
    """Tests for the document upload endpoint."""

    def test_upload_requires_file(self, client):
        """Test that upload requires a file."""
        response = client.post("/upload")
        assert response.status_code == 422

    def test_upload_rejects_non_pdf(self, client):
        """Test that non-PDF files are rejected."""
        files = {"file": ("test.txt", b"content", "text/plain")}
        response = client.post("/upload", files=files)
        assert response.status_code == 400
        assert "Only PDF files are supported" in response.json()["detail"]

    def test_upload_accepts_pdf(self, client):
        """Test that PDF files are accepted (mocked)."""
        with patch("backend.main.process_and_add_pdf", return_value=5) as mock_process:
            pdf_content = b"%PDF-1.4 test content"
            files = {"file": ("test.pdf", pdf_content, "application/pdf")}
            response = client.post("/upload", files=files)
            assert response.status_code == 200

    def test_upload_empty_filename_rejected(self, client):
        """Test that empty filenames are rejected (FastAPI validates first)."""
        pdf_content = b"%PDF-1.4 test content"
        files = {"file": ("", pdf_content, "application/pdf")}
        response = client.post("/upload", files=files)
        assert response.status_code == 422


class TestQueryEndpoint:
    """Tests for the query endpoint."""

    def test_query_requires_question(self, client):
        """Test that query requires a question."""
        response = client.post("/query", json={})
        assert response.status_code == 422

    def test_query_rejects_empty_question(self, client):
        """Test that empty question is rejected."""
        response = client.post("/query", json={"question": ""})
        assert response.status_code == 400

    def test_query_rejects_whitespace_only(self, client):
        """Test that whitespace-only question is rejected."""
        response = client.post("/query", json={"question": "   "})
        assert response.status_code == 400

    def test_query_returns_answer(self, client):
        """Test that query returns an answer (mocked)."""
        with patch("backend.main.query_rag") as mock_query:
            mock_query.return_value = {
                "answer": "Test answer",
                "sources": []
            }
            response = client.post("/query", json={"question": "What is test?"})
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "sources" in data
