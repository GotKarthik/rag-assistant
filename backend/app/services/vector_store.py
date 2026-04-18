"""
Vector store service — FAISS index management with metadata.
"""

import json
import os
import numpy as np
import faiss
from typing import Optional

from app.services.embeddings import get_embedding_dimension


class VectorStore:
    """
    Manages a FAISS index and associated chunk metadata.

    Uses IndexFlatIP (inner product) with L2-normalized vectors,
    which is equivalent to cosine similarity.
    """

    def __init__(self, index_dir: str, embedding_model: str = "all-MiniLM-L6-v2"):
        self.index_dir = index_dir
        self.embedding_model = embedding_model
        self.index_path = os.path.join(index_dir, "index.faiss")
        self.metadata_path = os.path.join(index_dir, "metadata.json")
        self.index: Optional[faiss.IndexFlatIP] = None
        self.metadata: list[dict] = []

    def _ensure_index(self):
        """Create index if it doesn't exist."""
        if self.index is None:
            dim = get_embedding_dimension(self.embedding_model)
            self.index = faiss.IndexFlatIP(dim)
            self.metadata = []

    def add_documents(self, embeddings: np.ndarray, chunks_metadata: list[dict]):
        """
        Add document embeddings and their metadata to the store.

        Args:
            embeddings: Numpy array of shape (n, dim), L2-normalized.
            chunks_metadata: List of dicts with chunk info (text, page, source, etc.)
        """
        self._ensure_index()

        # Ensure float32 for FAISS
        embeddings = embeddings.astype(np.float32)
        self.index.add(embeddings)
        self.metadata.extend(chunks_metadata)

        # Auto-save after adding
        self.save()

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list[dict]:
        """
        Search for the most similar chunks to the query.

        Args:
            query_embedding: Numpy array of shape (1, dim), L2-normalized.
            top_k: Number of results to return.

        Returns:
            List of dicts with keys: text, page, source, score, chunk_id.
        """
        self._ensure_index()

        if self.index.ntotal == 0:
            return []

        # Clamp top_k to available vectors
        actual_k = min(top_k, self.index.ntotal)
        query_embedding = query_embedding.astype(np.float32)

        scores, indices = self.index.search(query_embedding, actual_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            result = {**self.metadata[idx], "score": float(score)}
            results.append(result)

        return results

    def get_documents_by_id(self, document_id: str) -> list[dict]:
        """Get all chunk metadata for a specific document."""
        return [m for m in self.metadata if m.get("document_id") == document_id]

    def get_all_document_ids(self) -> list[dict]:
        """Get unique document info (id + filename)."""
        seen = {}
        for m in self.metadata:
            doc_id = m.get("document_id", "")
            if doc_id and doc_id not in seen:
                seen[doc_id] = {
                    "document_id": doc_id,
                    "filename": m.get("source", "unknown"),
                }
        return list(seen.values())

    def get_chunk_count(self, document_id: str = None) -> int:
        """Get total chunks, optionally filtered by document_id."""
        if document_id:
            return len([m for m in self.metadata if m.get("document_id") == document_id])
        return len(self.metadata)

    def save(self):
        """Persist FAISS index and metadata to disk."""
        os.makedirs(self.index_dir, exist_ok=True)

        if self.index is not None:
            faiss.write_index(self.index, self.index_path)

        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def load(self):
        """Load FAISS index and metadata from disk."""
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            print("[VectorStore] Loading existing index from disk...")
            self.index = faiss.read_index(self.index_path)

            with open(self.metadata_path, "r") as f:
                self.metadata = json.load(f)

            print(f"[VectorStore] Loaded {self.index.ntotal} vectors, {len(self.metadata)} metadata entries.")
        else:
            print("[VectorStore] No existing index found. Starting fresh.")
            self._ensure_index()

    def clear(self):
        """Clear the entire index and metadata."""
        dim = get_embedding_dimension(self.embedding_model)
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []
        self.save()


# Module-level singleton
_store: Optional[VectorStore] = None


def get_vector_store(index_dir: str, embedding_model: str = "all-MiniLM-L6-v2") -> VectorStore:
    """Get or create the singleton VectorStore instance."""
    global _store

    if _store is None:
        _store = VectorStore(index_dir, embedding_model)
        _store.load()

    return _store
