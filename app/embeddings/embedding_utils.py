# ============================================
# EMBEDDING UTILITIES
# ============================================

import numpy as np
from app.utils.logger import logger


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Returns:
        Float between 0 and 1 (1 = identical)
    """
    a = np.array(vec1)
    b = np.array(vec2)

    dot_product = np.dot(a, b)
    norm_a      = np.linalg.norm(a)
    norm_b      = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


def batch_texts(
    texts:      list[str],
    batch_size: int = 32,
) -> list[list[str]]:
    """
    Split texts into batches for processing.

    Args:
        texts:      List of texts
        batch_size: Size of each batch

    Returns:
        List of batches
    """
    batches = []
    for i in range(0, len(texts), batch_size):
        batches.append(texts[i:i + batch_size])
    return batches


def validate_embeddings(embeddings: list[list[float]]) -> bool:
    """
    Validate that embeddings are properly formed.

    Returns:
        True if valid, False otherwise
    """
    if not embeddings:
        logger.warning("Empty embeddings list")
        return False

    expected_dim = len(embeddings[0])
    for i, emb in enumerate(embeddings):
        if len(emb) != expected_dim:
            logger.error(
                f"Embedding {i} has wrong dimension: "
                f"{len(emb)} vs expected {expected_dim}"
            )
            return False

    return True