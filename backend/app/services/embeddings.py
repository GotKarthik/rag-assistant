"""
Embeddings service — sentence-transformers wrapper.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

from typing import Optional

# Module-level singleton
_model: Optional[SentenceTransformer] = None
_model_name: str = ""


def load_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    Load the embedding model (singleton — loaded once, reused).

    Args:
        model_name: HuggingFace model identifier.

    Returns:
        The loaded SentenceTransformer model.
    """
    global _model, _model_name

    if _model is None or _model_name != model_name:
        print(f"[Embeddings] Loading model: {model_name}")
        _model = SentenceTransformer(model_name)
        _model_name = model_name
        print(f"[Embeddings] Model loaded. Dimension: {_model.get_sentence_embedding_dimension()}")

    return _model


def embed_texts(texts: list[str], model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """
    Generate embeddings for a batch of texts.

    Args:
        texts: List of text strings to embed.
        model_name: Embedding model to use.

    Returns:
        Numpy array of shape (len(texts), embedding_dim).
    """
    model = load_model(model_name)
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)

    # L2 normalize for cosine similarity via inner product
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1  # avoid division by zero
    embeddings = embeddings / norms

    return embeddings


def embed_query(query: str, model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """
    Generate embedding for a single query string.

    Args:
        query: The query text.
        model_name: Embedding model to use.

    Returns:
        Numpy array of shape (1, embedding_dim).
    """
    return embed_texts([query], model_name)


def get_embedding_dimension(model_name: str = "all-MiniLM-L6-v2") -> int:
    """Get the dimensionality of embeddings from the model."""
    model = load_model(model_name)
    return model.get_sentence_embedding_dimension()
