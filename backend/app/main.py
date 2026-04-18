"""
FastAPI main application — entry point for the RAG Research Assistant API.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings, ensure_directories
from app.services.embeddings import load_model
from app.services.vector_store import get_vector_store
from app.routers import upload, query, summarize


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler — runs on startup and shutdown.

    Startup:
        - Create required data directories
        - Pre-load the embedding model into memory
        - Load existing FAISS index from disk (if any)
    """
    print("=" * 60)
    print("  RAG Research Assistant — Starting up...")
    print("=" * 60)

    # Create directories
    ensure_directories()

    # Pre-load embedding model (avoids cold-start on first request)
    print("[Startup] Loading embedding model...")
    load_model(settings.embedding_model)

    # Load existing vector store
    print("[Startup] Loading vector store...")
    get_vector_store(settings.index_dir, settings.embedding_model)

    print("[Startup] Ready!")
    print(f"[Config] Embedding model: {settings.embedding_model}")
    print(f"[Config] LLM model: {settings.llm_model}")
    print(f"[Config] Chunk size: {settings.chunk_size}, Overlap: {settings.chunk_overlap}")
    print(f"[Config] Top-K: {settings.top_k}, Threshold: {settings.similarity_threshold}")
    print("=" * 60)

    yield  # App runs here

    print("\n[Shutdown] RAG Research Assistant stopped.")


# ─── Create App ───────────────────────────────────────────

app = FastAPI(
    title="RAG Research Assistant",
    description="AI-powered research assistant using Retrieval-Augmented Generation. Upload PDFs, ask questions, get cited answers.",
    version="1.0.0",
    lifespan=lifespan,
)

# ─── CORS ─────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────

app.include_router(upload.router, tags=["Upload"])
app.include_router(query.router, tags=["Query"])
app.include_router(summarize.router, tags=["Summarize"])


# ─── Health Check ─────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    store = get_vector_store(settings.index_dir, settings.embedding_model)
    return {
        "status": "healthy",
        "documents": len(store.get_all_document_ids()),
        "total_chunks": store.get_chunk_count(),
    }


@app.get("/documents")
async def list_documents():
    """List all uploaded documents."""
    store = get_vector_store(settings.index_dir, settings.embedding_model)
    docs = store.get_all_document_ids()
    return {
        "documents": [
            {
                "document_id": d["document_id"],
                "filename": d["filename"],
                "num_chunks": store.get_chunk_count(d["document_id"]),
            }
            for d in docs
        ]
    }
