"""
Agent service — lightweight router that decides between Q&A and summarization.

Design decision: Using a deterministic keyword-based router instead of a full
LangChain ReAct agent. For just two actions (answer vs summarize), a ReAct agent
would add latency, non-determinism, and complexity with no real benefit.
"""

import re


# Keywords that strongly indicate a summarization request
SUMMARIZE_KEYWORDS = [
    "summarize", "summary", "summarise", "overview",
    "brief", "briefing", "recap", "outline",
    "what is this document about", "what is this paper about",
    "key points", "key takeaways", "main points",
    "tldr", "tl;dr", "give me a summary",
]


def classify_intent(query: str) -> str:
    """
    Classify user intent as 'summarize' or 'query'.

    Uses keyword matching for fast, deterministic routing.
    For ambiguous cases, defaults to 'query' (the more general action).

    Args:
        query: The user's input text.

    Returns:
        Either 'summarize' or 'query'.
    """
    query_lower = query.lower().strip()

    # Check for summarization keywords
    for keyword in SUMMARIZE_KEYWORDS:
        if keyword in query_lower:
            return "summarize"

    # Check for question patterns (explicit questions default to query)
    question_patterns = [
        r"^(what|who|where|when|why|how|which|is|are|do|does|did|can|could|should|would)\b",
        r"\?$",
    ]
    for pattern in question_patterns:
        if re.search(pattern, query_lower):
            return "query"

    # Default to query for anything else
    return "query"
