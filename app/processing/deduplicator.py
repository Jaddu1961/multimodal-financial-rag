# ============================================
# DEDUPLICATOR
# Prevents duplicate document ingestion
# ============================================

import json
from pathlib import Path
from app.utils.logger import logger


# Path to store ingested document hashes
REGISTRY_PATH = Path("./data/processed/ingested_docs.json")


def load_registry() -> dict:
    """Load the registry of already ingested documents"""
    if not REGISTRY_PATH.exists():
        return {}
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)


def save_registry(registry: dict) -> None:
    """Save the registry to disk"""
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


def is_duplicate(document_id: str, filename: str) -> bool:
    """
    Check if a document has already been ingested.

    Args:
        document_id: MD5 hash of the file
        filename:    Original filename

    Returns:
        True if already ingested, False if new
    """
    registry = load_registry()

    if document_id in registry:
        logger.warning(
            f"⚠️  Duplicate detected: {filename} "
            f"(already ingested on {registry[document_id]['ingested_at']})"
        )
        return True

    return False


def register_document(document_id: str, filename: str) -> None:
    """
    Mark a document as ingested in the registry.

    Args:
        document_id: MD5 hash of the file
        filename:    Original filename
    """
    import time

    registry = load_registry()
    registry[document_id] = {
        "filename":    filename,
        "ingested_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_registry(registry)
    logger.info(f"📋 Registered document: {filename}")