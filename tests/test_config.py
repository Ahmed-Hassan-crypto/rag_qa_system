import os
import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def clear_cache():
    """Clear settings cache before each test."""
    from backend.config import get_settings
    get_settings.cache_clear()
    yield


class TestSettings:
    """Tests for configuration settings."""

    def test_default_values(self):
        """Test that default values are set correctly."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"}):
            from backend.config import Settings
            settings = Settings()
            assert settings.embedding_model == "all-mpnet-base-v2"
            assert settings.llm_model == "gemini-2.0-flash"
            assert settings.llm_temperature == 0.0
            assert settings.chunk_size == 1000
            assert settings.chunk_overlap == 200
            assert settings.retriever_k == 5

    def test_custom_values(self):
        """Test that custom environment variables are loaded."""
        env = {
            "GOOGLE_API_KEY": "test_key",
            "EMBEDDING_MODEL": "custom-model",
            "LLM_MODEL": "custom-llm",
            "LLM_TEMPERATURE": "0.5",
            "CHUNK_SIZE": "500",
            "CHUNK_OVERLAP": "100",
            "RETRIEVER_K": "10",
        }
        with patch.dict(os.environ, env):
            from backend.config import Settings
            settings = Settings()
            assert settings.embedding_model == "custom-model"
            assert settings.llm_model == "custom-llm"
            assert settings.llm_temperature == 0.5
            assert settings.chunk_size == 500
            assert settings.chunk_overlap == 100
            assert settings.retriever_k == 10

    def test_validate_returns_false_without_api_key(self):
        """Test that validate returns False without API key."""
        with patch.dict(os.environ, {}, clear=True):
            from backend.config import Settings
            settings = Settings()
            assert settings.validate() is False

    def test_validate_settings_raises_error_without_api_key(self):
        """Test that validate_settings raises ValueError without API key."""
        with patch.dict(os.environ, {}, clear=True):
            from backend.config import validate_settings
            with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
                validate_settings()

    def test_debug_flag(self):
        """Test debug flag parsing."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key", "DEBUG": "true"}):
            from backend.config import Settings
            settings = Settings()
            assert settings.debug is True

        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key", "DEBUG": "false"}):
            from backend.config import Settings
            settings = Settings()
            assert settings.debug is False
