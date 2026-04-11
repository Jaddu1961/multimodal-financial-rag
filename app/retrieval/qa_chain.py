# ============================================
# QA CHAIN
# Generates answers using retrieved context
# ============================================

from app.retrieval.retriever import retrieve
from app.retrieval.prompt_templates import (
    RAG_SYSTEM_PROMPT,
    RAG_USER_PROMPT,
    NO_CONTEXT_RESPONSE,
)
from app.llm.groq_client import generate_answer
from app.utils.logger import logger
from config.settings import settings


def answer_question(
    question:    str,
    n_results:   int  = None,
    filter_type: str  = None,
    filter_doc:  str  = None,
) -> dict:
    """
    Answer a question using RAG pipeline with Groq.

    Args:
        question:    User's question
        n_results:   Number of chunks to retrieve
        filter_type: Optional chunk type filter
        filter_doc:  Optional document filter

    Returns:
        Dict with answer, sources, and metadata
    """
    logger.info(f"💬 Processing question: '{question[:60]}'")

    # --- Step 1: Retrieve relevant context ---
    retrieval_result = retrieve(
        query       = question,
        n_results   = n_results,
        filter_type = filter_type,
        filter_doc  = filter_doc,
    )

    # --- Step 2: Handle no context case ---
    if not retrieval_result["chunks"]:
        logger.warning("⚠️  No context found — returning default response")
        return {
            "answer":            NO_CONTEXT_RESPONSE,
            "sources":           [],
            "types_used":        {},
            "total_chunks_used": 0,
            "question":          question,
        }

    # --- Step 3: Build user prompt ---
    user_prompt = RAG_USER_PROMPT.format(
        context  = retrieval_result["formatted_context"],
        question = question,
    )

    # --- Step 4: Generate answer with Groq ---
    answer = generate_answer(
        system_prompt = RAG_SYSTEM_PROMPT,
        user_prompt   = user_prompt,
    )

    # --- Step 5: Format sources ---
    sources = []
    for chunk in retrieval_result["chunks"]:
        sources.append({
            "chunk_type":  chunk["metadata"].get("chunk_type"),
            "page_number": chunk["metadata"].get("page_number"),
            "source_file": chunk["metadata"].get("source_file"),
            "relevance":   round(chunk.get("score", 0), 3),
            "preview":     chunk["text"][:150] + "..."
                           if len(chunk["text"]) > 150
                           else chunk["text"],
        })

    logger.info("✅ Answer generated successfully")

    return {
        "answer":            answer,
        "sources":           sources,
        "types_used":        retrieval_result["types_found"],
        "total_chunks_used": retrieval_result["total_found"],
        "question":          question,
    }