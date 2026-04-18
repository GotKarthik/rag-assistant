"""
Pydantic models for API request/response schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ─── Upload ───────────────────────────────────────────────

class UploadResponse(BaseModel):
    """Response after successfully uploading and processing a PDF."""
    document_id: str
    filename: str
    num_chunks: int
    message: str


# ─── Query ────────────────────────────────────────────────

class QueryRequest(BaseModel):
    """Request body for the /query endpoint."""
    question: str = Field(..., min_length=1, description="The question to answer")
    top_k: Optional[int] = Field(None, ge=1, le=20, description="Number of chunks to retrieve")


class SourceChunk(BaseModel):
    """A single source chunk used as evidence."""
    text: str
    page: int
    source: str
    score: float


class QueryResponse(BaseModel):
    """Response from the /query endpoint."""
    answer: str
    sources: list[SourceChunk]


# ─── Summarize ────────────────────────────────────────────

class SummarizeRequest(BaseModel):
    """Request body for the /summarize endpoint."""
    document_id: Optional[str] = Field(None, description="Specific document to summarize (omit for all)")


class SummarizeResponse(BaseModel):
    """Response from the /summarize endpoint."""
    summary: str
    sources: list[SourceChunk]


# ─── Documents ────────────────────────────────────────────

class DocumentInfo(BaseModel):
    """Info about an uploaded document."""
    document_id: str
    filename: str
    num_chunks: int
