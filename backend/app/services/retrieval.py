"""
Retrieval service — orchestrates embedding queries and FAISS search.
"""

from app.services.embeddings import embed_query
from app.services.vector_store import VectorStore


def retrieve(
    query: str,
    vector_store: VectorStore,
    top_k: int = 5,
    similarity_threshold: float = 0.3,
    embedding_model: str = "all-MiniLM-L6-v2",
) -> list[dict]:
    """
    Retrieve the most relevant chunks for a given query.

    Pipeline:
        1. Embed the query using the same model used for document embeddings
        2. Search the FAISS index for top-k similar vectors
        3. Filter results below the similarity threshold

    Args:
        query: The user's question or search query.
        vector_store: The VectorStore instance to search.
        top_k: Number of results to retrieve.
        similarity_threshold: Minimum cosine similarity score to include a result.
        embedding_model: Model name for generating query embeddings.

    Returns:
        List of result dicts: {text, page, source, score, chunk_id, document_id}
    """
    # 1. Embed the query
    query_embedding = embed_query(query, embedding_model)

    # 2. Search FAISS
    raw_results = vector_store.search(query_embedding, top_k)

    # 3. Filter by similarity threshold
    filtered = [r for r in raw_results if r["score"] >= similarity_threshold]

    return filtered


def retrieve_by_document(
    vector_store: VectorStore,
    document_id: str = None,
    max_chunks: int = 20,
) -> list[dict]:
    """
    Retrieve chunks for summarization — either all chunks or filtered by document.

    Unlike query-based retrieval, this returns chunks directly from metadata
    without embedding-based search (since we want to summarize the full document,
    not find the most relevant chunks for a specific question).

    Args:
        vector_store: The VectorStore instance.
        document_id: Optional document ID to filter by.
        max_chunks: Maximum number of chunks to return.

    Returns:
        List of chunk dicts.
    """
    if document_id:
        chunks = vector_store.get_documents_by_id(document_id)
    else:
        chunks = vector_store.metadata.copy()

    # Sort by page number for coherent summarization
    chunks.sort(key=lambda c: (c.get("source", ""), c.get("page", 0)))

    # Limit to max_chunks to avoid exceeding LLM context window
    return chunks[:max_chunks]
