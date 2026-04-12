# ============================================
# RETRIEVER
# Enhanced retrieval with reranking
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
    Retrieve relevant chunks with smart reranking.

    Args:
        query:       User's question
        n_results:   Number of chunks to retrieve
        filter_type: Optional filter by type
        filter_doc:  Optional filter by document ID

    Returns:
        Dict with chunks and formatted context
    """
    if n_results is None:
        n_results = settings.TOP_K_RESULTS

    logger.info(f"🔍 Retrieving context for: '{query[:60]}'")

    # --- Step 1: Get more candidates than needed ---
    # Retrieve 2x results then rerank for better quality
    candidate_count = min(n_results * 2, 20)

    chunks = search(
        query       = query,
        n_results   = candidate_count,
        filter_type = filter_type,
        filter_doc  = filter_doc,
    )

    if not chunks:
        logger.warning("⚠️  No relevant chunks found")
        return {
            "chunks":            [],
            "formatted_context": "No relevant context found.",
            "total_found":       0,
            "types_found":       {},
        }

    # --- Step 2: Rerank by multiple signals ---
    reranked = _rerank_chunks(query, chunks)

    # --- Step 3: Take top n_results after reranking ---
    final_chunks = reranked[:n_results]

    # --- Step 4: Ensure diversity of chunk types ---
    final_chunks = _ensure_type_diversity(final_chunks, reranked, n_results)

    # --- Step 5: Format context ---
    formatted_context = format_context(final_chunks)

    # --- Count chunk types ---
    types_found = {}
    for chunk in final_chunks:
        chunk_type = chunk["metadata"].get("chunk_type", "unknown")
        types_found[chunk_type] = types_found.get(chunk_type, 0) + 1

    logger.info(
        f"✅ Retrieved {len(final_chunks)} chunks after reranking: "
        f"{types_found}"
    )

    return {
        "chunks":            final_chunks,
        "formatted_context": formatted_context,
        "total_found":       len(final_chunks),
        "types_found":       types_found,
    }


def _rerank_chunks(query: str, chunks: list[dict]) -> list[dict]:
    """
    Rerank chunks using multiple signals:
    1. Semantic similarity score
    2. Keyword overlap with query
    3. Chunk type bonus (graphs get boost for trend questions)

    Args:
        query:  User query
        chunks: Initial retrieved chunks

    Returns:
        Reranked list of chunks
    """
    query_words = set(query.lower().split())

    # --- Keywords that suggest visual/trend data ---
    trend_keywords  = {'trend', 'chart', 'graph', 'show', 'visual',
                       'increase', 'decrease', 'growth', 'decline'}
    table_keywords  = {'revenue', 'margin', 'profit', 'income', 'expense',
                       'cost', 'cash', 'flow', 'earnings', 'loss'}

    is_trend_query = bool(query_words & trend_keywords)
    is_table_query = bool(query_words & table_keywords)

    scored_chunks = []
    for chunk in chunks:
        base_score   = chunk.get("score", 0)
        chunk_type   = chunk["metadata"].get("chunk_type", "text")
        chunk_text   = chunk["text"].lower()

        # --- Keyword overlap bonus ---
        chunk_words    = set(chunk_text.split())
        overlap        = len(query_words & chunk_words)
        keyword_bonus  = min(overlap * 0.02, 0.1)

        # --- Chunk type bonus ---
        type_bonus = 0
        if is_trend_query and chunk_type == "graph":
            type_bonus = 0.15  # Boost graphs for trend questions
        elif is_table_query and chunk_type == "table":
            type_bonus = 0.10  # Boost tables for financial questions

        # --- Length penalty (very short chunks are less useful) ---
        length_penalty = 0
        if len(chunk["text"]) < 100:
            length_penalty = 0.05

        # --- Final score ---
        final_score = base_score + keyword_bonus + type_bonus - length_penalty

        scored_chunks.append({
            **chunk,
            "rerank_score": final_score,
            "score":        final_score,
        })

    # Sort by rerank score
    return sorted(scored_chunks, key=lambda x: x["rerank_score"], reverse=True)


def _ensure_type_diversity(
    top_chunks:   list[dict],
    all_chunks:   list[dict],
    n_results:    int,
) -> list[dict]:
    """
    Ensure we have diversity of chunk types.
    If all top chunks are text, try to include
    at least one table and one graph if available.

    Args:
        top_chunks: Already selected top chunks
        all_chunks: All available chunks
        n_results:  Target number of results

    Returns:
        Diversified chunk list
    """
    types_present = {
        c["metadata"].get("chunk_type")
        for c in top_chunks
    }

    final = list(top_chunks)

    # --- Try to add a table if none present ---
    if "table" not in types_present and len(final) < n_results:
        table_chunks = [
            c for c in all_chunks
            if c["metadata"].get("chunk_type") == "table"
            and c not in final
        ]
        if table_chunks:
            final.append(table_chunks[0])

    # --- Try to add a graph if none present ---
    if "graph" not in types_present and len(final) < n_results:
        graph_chunks = [
            c for c in all_chunks
            if c["metadata"].get("chunk_type") == "graph"
            and c not in final
        ]
        if graph_chunks:
            final.append(graph_chunks[0])

    return final[:n_results]


def retrieve_by_type(query: str, chunk_type: str) -> dict:
    """
    Retrieve chunks of a specific type only.
    """
    return retrieve(query=query, filter_type=chunk_type)