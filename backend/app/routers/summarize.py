"""
Summarize router — handles document summarization.
"""

from fastapi import APIRouter, HTTPException

from app.config import settings
from app.models import SummarizeRequest, SummarizeResponse, SourceChunk
from app.services.retrieval import retrieve_by_document
from app.services.llm import generate_summary
from app.services.vector_store import get_vector_store

router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_documents(request: SummarizeRequest):
    """
    Generate a summary of uploaded documents.

    If a document_id is provided, summarize only that document.
    Otherwise, summarize all uploaded documents.
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

    # Retrieve chunks for summarization
    chunks = retrieve_by_document(
        vector_store=store,
        document_id=request.document_id,
        max_chunks=20,
    )

    if not chunks:
        raise HTTPException(
            status_code=404,
            detail=f"No chunks found for document_id: {request.document_id}"
        )

    # Generate summary via LLM
    try:
        summary = generate_summary(
            chunks=chunks,
            api_key=settings.groq_api_key,
            model=settings.llm_model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM summarization failed: {str(e)}")

    # Build source list (unique sources only)
    seen_sources = set()
    sources = []
    for chunk in chunks:
        source_key = f"{chunk['source']}_p{chunk['page']}"
        if source_key not in seen_sources:
            seen_sources.add(source_key)
            sources.append(
                SourceChunk(
                    text=chunk["text"][:200] + ("..." if len(chunk["text"]) > 200 else ""),
                    page=chunk["page"],
                    source=chunk["source"],
                    score=1.0,  # Direct retrieval, no similarity score
                )
            )

    return SummarizeResponse(summary=summary, sources=sources)
