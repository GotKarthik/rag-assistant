"""
LLM service — Groq API interface for answer generation and summarization.
"""

from groq import Groq


from typing import Optional

# Module-level client singleton
_client: Optional[Groq] = None


def _get_client(api_key: str) -> Groq:
    """Get or create the Groq client singleton."""
    global _client
    if _client is None:
        _client = Groq(api_key=api_key)
    return _client


def _format_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a context string for the LLM prompt."""
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("source", "unknown")
        page = chunk.get("page", "?")
        text = chunk.get("text", "")
        context_parts.append(
            f"[Source {i}: {source}, Page {page}]\n{text}"
        )
    return "\n\n---\n\n".join(context_parts)


def generate_answer(
    query: str,
    chunks: list[dict],
    api_key: str,
    model: str = "llama-3.3-70b-versatile",
) -> str:
    """
    Generate an answer to a question using retrieved context chunks.

    The LLM is prompted to:
    - Only use information from the provided context
    - Include inline citations in [Source: filename, Page X] format
    - Say "I don't have enough information" if context is insufficient

    Args:
        query: The user's question.
        chunks: Retrieved context chunks with metadata.
        api_key: Groq API key.
        model: LLM model identifier.

    Returns:
        The generated answer string with citations.
    """
    client = _get_client(api_key)

    if not chunks:
        return "I don't have enough information in the uploaded documents to answer this question. Please upload relevant documents first."

    context = _format_context(chunks)

    system_prompt = """You are a helpful research assistant. Answer the user's question based ONLY on the provided context from uploaded documents.

Rules:
1. Only use information from the provided context. Do NOT make up information.
2. Include inline citations using the format [Source: filename, Page X] after each claim.
3. If the context doesn't contain enough information to fully answer the question, say so clearly.
4. Be concise but thorough.
5. Use bullet points or numbered lists when appropriate for clarity."""

    user_prompt = f"""Context from uploaded documents:

{context}

---

Question: {query}

Please provide a well-cited answer based on the context above."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=2048,
    )

    return response.choices[0].message.content


def generate_summary(
    chunks: list[dict],
    api_key: str,
    model: str = "llama-3.3-70b-versatile",
) -> str:
    """
    Generate a summary of the provided document chunks.

    Args:
        chunks: Document chunks to summarize.
        api_key: Groq API key.
        model: LLM model identifier.

    Returns:
        The generated summary string with source references.
    """
    client = _get_client(api_key)

    if not chunks:
        return "No documents have been uploaded yet. Please upload a document first."

    context = _format_context(chunks)

    system_prompt = """You are a helpful research assistant. Summarize the provided document content clearly and comprehensively.

Rules:
1. Create a well-structured summary covering the main points, key findings, and important details.
2. Include source references using [Source: filename, Page X] format.
3. Organize the summary with clear sections if the content covers multiple topics.
4. Be thorough but concise — aim for a summary that captures the essential information.
5. Use bullet points for key takeaways."""

    user_prompt = f"""Document content to summarize:

{context}

---

Please provide a comprehensive summary of the above document content."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=2048,
    )

    return response.choices[0].message.content
