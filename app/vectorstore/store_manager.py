# ============================================
# STORE MANAGER
# High-level vector store operations
# ============================================

from app.processing.document_models import DocumentChunk
from app.embeddings.embedder import embed_texts
from app.embeddings.embedding_utils import validate_embeddings
from app.vectorstore.chroma_store import (
    add_chunks,
    query_similar,
    get_collection_stats,
    delete_document,
)
from app.embeddings.embedder import embed_single
from app.utils.logger import logger
from config.settings import settings


def store_chunks(chunks: list[DocumentChunk]) -> dict:
    """
    Embed and store a list of chunks in ChromaDB.

    Args:
        chunks: List of DocumentChunk objects to store

    Returns:
        Dict with storage results
    """
    if not chunks:
        logger.warning("No chunks to store")
        return {"stored": 0, "failed": 0}

    logger.info(f"💾 Storing {len(chunks)} chunks...")

    # --- Generate embeddings ---
    texts      = [chunk.text for chunk in chunks]
    embeddings = embed_texts(texts)

    # --- Validate embeddings ---
    if not validate_embeddings(embeddings):
        raise ValueError("Invalid embeddings generated")

    # --- Store in ChromaDB ---
    add_chunks(chunks=chunks, embeddings=embeddings)

    return {
        "stored": len(chunks),
        "failed": 0,
    }


def search(
    query:       str,
    n_results:   int  = None,
    filter_type: str  = None,
    filter_doc:  str  = None,
) -> list[dict]:
    """
    Search for relevant chunks using a text query.

    Args:
        query:       User's question or search text
        n_results:   Number of results (default from settings)
        filter_type: Optional filter: "text", "table", or "graph"
        filter_doc:  Optional filter by document_id

    Returns:
        List of relevant chunks with scores
    """
    if n_results is None:
        n_results = settings.TOP_K_RESULTS

    logger.info(f"🔍 Searching: '{query[:50]}...' " if len(query) > 50 else f"🔍 Searching: '{query}'")

    # --- Embed the query ---
    query_embedding = embed_single(query)

    # --- Search ChromaDB ---
    results = query_similar(
        query_embedding = query_embedding,
        n_results       = n_results,
        filter_type     = filter_type,
        filter_doc      = filter_doc,
    )

    logger.info(f"✅ Found {len(results)} relevant chunks")
    return results


def get_stats() -> dict:
    """Get current vector store statistics"""
    return get_collection_stats()


def remove_document(document_id: str) -> None:
    """Remove all chunks for a document from the store"""
    delete_document(document_id)