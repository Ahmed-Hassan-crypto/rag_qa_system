import os
from typing import Optional
from functools import lru_cache


class Settings:
    """Application configuration loaded from environment variables."""

    def __init__(self):
        self.google_api_key: Optional[str] = os.environ.get("GOOGLE_API_KEY")
        self.embedding_model: str = os.environ.get("EMBEDDING_MODEL", "all-mpnet-base-v2")
        self.llm_model: str = os.environ.get("LLM_MODEL", "gemini-2.0-flash")
        self.llm_temperature: float = float(os.environ.get("LLM_TEMPERATURE", "0.0"))
        self.chroma_path: str = os.environ.get("CHROMA_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db"))
        self.chunk_size: int = int(os.environ.get("CHUNK_SIZE", "1000"))
        self.chunk_overlap: int = int(os.environ.get("CHUNK_OVERLAP", "200"))
        self.retriever_k: int = int(os.environ.get("RETRIEVER_K", "5"))
        self.backend_host: str = os.environ.get("BACKEND_HOST", "127.0.0.1")
        self.backend_port: int = int(os.environ.get("BACKEND_PORT", "8000"))
        self.frontend_port: int = int(os.environ.get("FRONTEND_PORT", "8501"))
        self.debug: bool = os.environ.get("DEBUG", "false").lower() == "true"

    def validate(self) -> bool:
        """Validate required configuration. Returns True if valid, False otherwise."""
        return bool(self.google_api_key)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


def validate_settings() -> None:
    """Validate required settings, raise error if invalid."""
    settings = get_settings()
    if not settings.validate():
        raise ValueError("GOOGLE_API_KEY environment variable is required. Copy .env.example to .env and add your key.")
