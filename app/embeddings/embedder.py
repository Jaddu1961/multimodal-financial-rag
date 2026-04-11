# ============================================
# EMBEDDER
# Converts text into vector embeddings
# ============================================

from sentence_transformers import SentenceTransformer
from app.utils.logger import logger
from config.settings import settings
from config.model_config import EMBEDDING_CONFIG
import numpy as np


# --- Singleton model instance ---
_model = None


def get_embedding_model() -> SentenceTransformer:
    """
    Load and return the embedding model.
    Uses singleton pattern — loads only once.

    Returns:
        SentenceTransformer model instance
    """
    global _model

    if _model is None:
        logger.info(f"🔄 Loading embedding model: {EMBEDDING_CONFIG['model_name']}")
        _model = SentenceTransformer(
            EMBEDDING_CONFIG["model_name"],
            device=EMBEDDING_CONFIG["device"],
        )
        logger.info(f"✅ Embedding model loaded successfully")

    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of texts.

    Args:
        texts: List of strings to embed

    Returns:
        List of embedding vectors (each is a list of floats)
    """
    if not texts:
        return []

    model = get_embedding_model()

    logger.info(f"🔢 Generating embeddings for {len(texts)} texts...")

    # --- Generate embeddings in batches ---
    embeddings = model.encode(
        texts,
        batch_size          = EMBEDDING_CONFIG["batch_size"],
        normalize_embeddings= EMBEDDING_CONFIG["normalize_embeddings"],
        show_progress_bar   = len(texts) > 10,
    )

    # Convert numpy arrays to Python lists for ChromaDB
    embeddings_list = embeddings.tolist()

    logger.info(f"✅ Generated {len(embeddings_list)} embeddings")
    logger.info(f"   Embedding dimension: {len(embeddings_list[0])}")

    return embeddings_list


def embed_single(text: str) -> list[float]:
    """
    Generate embedding for a single text.
    Used for embedding user queries.

    Args:
        text: String to embed

    Returns:
        Single embedding vector
    """
    return embed_texts([text])[0]