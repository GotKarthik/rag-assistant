"""
Upload router — handles PDF file uploads and processing.
"""

import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.config import settings, ensure_directories
from app.models import UploadResponse
from app.services.ingestion import process_pdf
from app.services.embeddings import embed_texts
from app.services.vector_store import get_vector_store

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF document for processing.

    Pipeline:
        1. Validate file type
        2. Save file to disk
        3. Extract and chunk text
        4. Generate embeddings
        5. Store in FAISS index
    """
    # Validate file type
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported. Please upload a .pdf file."
        )

    # Ensure directories exist
    ensure_directories()

    # Save uploaded file
    file_path = os.path.join(settings.upload_dir, file.filename)
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Process the PDF
    try:
        document_id, chunks = process_pdf(
            file_path,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
    except Exception as e:
        # Clean up the file if processing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    if not chunks:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail="Could not extract any text from the PDF. The file may be image-based or empty."
        )

    # Generate embeddings
    try:
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embed_texts(texts, settings.embedding_model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embeddings: {str(e)}")

    # Store in vector database
    try:
        store = get_vector_store(settings.index_dir, settings.embedding_model)
        store.add_documents(embeddings, chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store embeddings: {str(e)}")

    return UploadResponse(
        document_id=document_id,
        filename=file.filename,
        num_chunks=len(chunks),
        message=f"Successfully processed '{file.filename}' into {len(chunks)} chunks.",
    )
