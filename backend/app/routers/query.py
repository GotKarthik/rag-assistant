"""
Query router — handles question-answering over uploaded documents.
"""

from fastapi import APIRouter, HTTPException

from app.config import settings
from app.models import QueryRequest, QueryResponse, SourceChunk
from app.services.retrieval import retrieve
from app.services.llm import generate_answer
from app.services.vector_store import get_vector_store

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Answer a question using the RAG pipeline.

    Pipeline:
        1. Retrieve top-k relevant chunks from FAISS
        2. Pass chunks as context to the LLM
        3. LLM generates a cited answer
        4. Return answer + source chunks
    """
    if not settings.groq_api_key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not configured. Please set it in your environment variables."
        )

    # Get vector store
    store = get_vector_store(settings.index_dir, settings.embedding_model)

    if store.get_chunk_count() == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents have been uploaded yet. Please upload a PDF first."
        )

    # Retrieve relevant chunks
    top_k = request.top_k or settings.top_k
    chunks = retrieve(
        query=request.question,
        vector_store=store,
        top_k=top_k,
        similarity_threshold=settings.similarity_threshold,
        embedding_model=settings.embedding_model,
    )

    # Generate answer via LLM
    try:
        answer = generate_answer(
            query=request.question,
            chunks=chunks,
            api_key=settings.groq_api_key,
            model=settings.llm_model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {str(e)}")

    # Build source list
    sources = [
        SourceChunk(
            text=chunk["text"][:300] + ("..." if len(chunk["text"]) > 300 else ""),
            page=chunk["page"],
            source=chunk["source"],
            score=round(chunk["score"], 4),
        )
        for chunk in chunks
    ]

    return QueryResponse(answer=answer, sources=sources)
