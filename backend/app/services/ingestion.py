"""
Ingestion service — PDF text extraction and chunking.
"""

import fitz  # PyMuPDF
import uuid
import os
from pathlib import Path


def extract_text(pdf_path: str) -> list[dict]:
    """
    Extract text from each page of a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        List of dicts with keys: text, page (1-indexed), source (filename).
    """
    doc = fitz.open(pdf_path)
    filename = Path(pdf_path).name
    pages = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text").strip()
        if text:
            pages.append({
                "text": text,
                "page": page_num + 1,  # 1-indexed
                "source": filename,
            })

    doc.close()
    return pages


def chunk_text(
    pages: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[dict]:
    """
    Split extracted text into overlapping chunks while preserving metadata.

    Each chunk retains the source filename and page number it originated from.
    Chunks are created by sliding a window over the text with the given size
    and overlap.

    Args:
        pages: List of page dicts from extract_text().
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of overlapping characters between consecutive chunks.

    Returns:
        List of chunk dicts with keys: text, page, source, chunk_id.
    """
    chunks = []

    for page_data in pages:
        text = page_data["text"]
        page = page_data["page"]
        source = page_data["source"]

        # Slide a window over the text
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text_str = text[start:end].strip()

            if chunk_text_str:
                chunks.append({
                    "text": chunk_text_str,
                    "page": page,
                    "source": source,
                    "chunk_id": str(uuid.uuid4()),
                })

            # Move window forward
            start += chunk_size - chunk_overlap

            # Avoid tiny trailing chunks
            if len(text) - start < chunk_overlap:
                break

    return chunks


def process_pdf(
    pdf_path: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> tuple[str, list[dict]]:
    """
    Full pipeline: extract text from PDF and chunk it.

    Args:
        pdf_path: Path to the PDF file.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Overlap between chunks.

    Returns:
        Tuple of (document_id, list of chunk dicts).
    """
    document_id = str(uuid.uuid4())
    pages = extract_text(pdf_path)
    chunks = chunk_text(pages, chunk_size, chunk_overlap)

    # Tag each chunk with the document_id
    for chunk in chunks:
        chunk["document_id"] = document_id

    return document_id, chunks
