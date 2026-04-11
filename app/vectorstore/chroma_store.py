# ============================================
# CHROMA VECTOR STORE
# Stores and retrieves embeddings
# ============================================

import chromadb
from chromadb.config import Settings as ChromaSettings
from app.processing.document_models import DocumentChunk
from app.utils.logger import logger
from config.settings import settings
from config.model_config import CHROMA_CONFIG


# --- Singleton client instance ---
_client     = None
_collection = None


def get_chroma_client() -> chromadb.PersistentClient:
    """
    Get or create ChromaDB persistent client.
    Uses singleton pattern.

    Returns:
        ChromaDB PersistentClient
    """
    global _client

    if _client is None:
        logger.info(f"🔄 Connecting to ChromaDB: {CHROMA_CONFIG['persist_directory']}")

        _client = chromadb.PersistentClient(
            path    = CHROMA_CONFIG["persist_directory"],
            settings= ChromaSettings(anonymized_telemetry=False),
        )

        logger.info("✅ ChromaDB client connected")

    return _client


def get_collection() -> chromadb.Collection:
    """
    Get or create the main ChromaDB collection.

    Returns:
        ChromaDB Collection
    """
    global _collection

    if _collection is None:
        client = get_chroma_client()

        _collection = client.get_or_create_collection(
            name     = CHROMA_CONFIG["collection_name"],
            metadata = {"hnsw:space": CHROMA_CONFIG["distance_metric"]},
        )

        logger.info(
            f"✅ Collection ready: {CHROMA_CONFIG['collection_name']} "
            f"({_collection.count()} existing documents)"
        )

    return _collection


def add_chunks(
    chunks:     list[DocumentChunk],
    embeddings: list[list[float]],
) -> None:
    """
    Add document chunks with their embeddings to ChromaDB.

    Args:
        chunks:     List of DocumentChunk objects
        embeddings: Corresponding embedding vectors
    """
    if not chunks:
        logger.warning("No chunks to add")
        return

    if len(chunks) != len(embeddings):
        raise ValueError(
            f"Chunks ({len(chunks)}) and embeddings "
            f"({len(embeddings)}) must have same length"
        )

    collection = get_collection()

    # --- Prepare data for ChromaDB ---
    ids        = [chunk.chunk_id for chunk in chunks]
    documents  = [chunk.text for chunk in chunks]
    metadatas  = [chunk.to_metadata() for chunk in chunks]

    # --- Add to ChromaDB in batches ---
    batch_size = 100
    total      = len(chunks)

    for i in range(0, total, batch_size):
        batch_end = min(i + batch_size, total)

        collection.add(
            ids        = ids[i:batch_end],
            documents  = documents[i:batch_end],
            embeddings = embeddings[i:batch_end],
            metadatas  = metadatas[i:batch_end],
        )

        logger.debug(f"   Added batch {i//batch_size + 1}: {batch_end}/{total} chunks")

    logger.info(f"✅ Added {total} chunks to ChromaDB")
    logger.info(f"   Total in collection: {collection.count()}")


def query_similar(
    query_embedding: list[float],
    n_results:       int  = None,
    filter_type:     str  = None,
    filter_doc:      str  = None,
) -> list[dict]:
    """
    Find most similar chunks to a query embedding.

    Args:
        query_embedding: Embedding vector of the query
        n_results:       Number of results to return
        filter_type:     Optional filter by chunk type (text/table/graph)
        filter_doc:      Optional filter by document_id

    Returns:
        List of dicts with text, metadata, and distance
    """
    if n_results is None:
        n_results = settings.TOP_K_RESULTS

    collection = get_collection()

    # --- Build optional filters ---
    where = {}
    if filter_type:
        where["chunk_type"] = {"$eq": filter_type}
    if filter_doc:
        where["document_id"] = {"$eq": filter_doc}

    # --- Query ChromaDB ---
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results        = n_results,
        where            = where if where else None,
        include          = ["documents", "metadatas", "distances"],
    )

    # --- Format results ---
    formatted = []
    if results and results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            formatted.append({
                "text":     doc,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "score":    1 - results["distances"][0][i],  # Convert to similarity
            })

    logger.debug(f"🔍 Retrieved {len(formatted)} chunks for query")
    return formatted


def get_collection_stats() -> dict:
    """
    Get statistics about the current collection.

    Returns:
        Dict with collection statistics
    """
    collection = get_collection()
    total      = collection.count()

    return {
        "collection_name": CHROMA_CONFIG["collection_name"],
        "total_chunks":    total,
        "persist_path":    CHROMA_CONFIG["persist_directory"],
    }


def delete_document(document_id: str) -> None:
    """
    Delete all chunks for a specific document.

    Args:
        document_id: Document ID to delete
    """
    collection = get_collection()

    collection.delete(
        where={"document_id": {"$eq": document_id}}
    )

    logger.info(f"🗑️  Deleted all chunks for document: {document_id}")