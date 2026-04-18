"""
Configuration module — loads settings from environment variables.
"""

import os
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- API Keys ---
    groq_api_key: str = ""

    # --- Model Settings ---
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "llama-3.3-70b-versatile"

    # --- Chunking Settings ---
    chunk_size: int = 500
    chunk_overlap: int = 100

    # --- Retrieval Settings ---
    top_k: int = 5
    similarity_threshold: float = 0.3

    # --- Paths ---
    data_dir: str = str(Path(__file__).parent / "data")
    upload_dir: str = str(Path(__file__).parent / "data" / "uploads")
    index_dir: str = str(Path(__file__).parent / "data" / "faiss_index")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


# Singleton settings instance
settings = Settings()


def ensure_directories():
    """Create required data directories if they don't exist."""
    for dir_path in [settings.data_dir, settings.upload_dir, settings.index_dir]:
        os.makedirs(dir_path, exist_ok=True)
