# ============================================
# RETRIEVER
# Finds relevant chunks for a user query
# ============================================

from app.vectorstore.store_manager import search
from app.retrieval.prompt_templates import format_context
from app.utils.logger import logger
from config.settings import settings


def retrieve(
    query:       str,
    n_results:   int  = None,
    filter_type: str  = None,
    filter_doc:  str  = None,
) -> dict:
    """
    Retrieve relevant chunks for a user query.

    Args:
        query:       User's question
        n_results:   Number of chunks to retrieve
        filter_type: Optional filter by type (text/table/graph)
        filter_doc:  Optional filter by document ID

    Returns:
        Dict with chunks and formatted context
    """
    if n_results is None:
        n_results = settings.TOP_K_RESULTS

    logger.info(f"🔍 Retrieving context for: '{query[:60]}'")

    # --- Search vector store ---
    chunks = search(
        query       = query,
        n_results   = n_results,
        filter_type = filter_type,
        filter_doc  = filter_doc,
    )

    if not chunks:
        logger.warning("⚠️  No relevant chunks found")
        return {
            "chunks":          [],
            "formatted_context": "No relevant context found.",
            "total_found":     0,
            "types_found":     {},
        }

    # --- Filter by similarity threshold ---
    threshold = settings.SIMILARITY_THRESHOLD
    filtered  = [c for c in chunks if c.get("score", 0) >= threshold]

    if not filtered:
        logger.warning(
            f"⚠️  All chunks below similarity threshold ({threshold}). "
            f"Using top results anyway."
        )
        filtered = chunks[:3]  # Use top 3 regardless

    # --- Format context for LLM ---
    formatted_context = format_context(filtered)

    # --- Count chunk types ---
    types_found = {}
    for chunk in filtered:
        chunk_type = chunk["metadata"].get("chunk_type", "unknown")
        types_found[chunk_type] = types_found.get(chunk_type, 0) + 1

    logger.info(
        f"✅ Retrieved {len(filtered)} chunks: "
        f"{types_found}"
    )

    return {
        "chunks":            filtered,
        "formatted_context": formatted_context,
        "total_found":       len(filtered),
        "types_found":       types_found,
    }


def retrieve_by_type(query: str, chunk_type: str) -> dict:
    """
    Retrieve chunks of a specific type only.

    Args:
        query:      User's question
        chunk_type: "text", "table", or "graph"

    Returns:
        Dict with chunks and formatted context
    """
    return retrieve(query=query, filter_type=chunk_type)