# ============================================
# DOCUMENTS ROUTER
# Lists and manages ingested documents
# ============================================

from fastapi import APIRouter, HTTPException
from app.api.schemas.ingest_schema import DocumentListResponse, DocumentInfo
from app.processing.deduplicator import load_registry
from app.utils.logger import logger


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/list", response_model=DocumentListResponse)
async def list_documents():
    """
    List all ingested documents.

    Returns document IDs, filenames, and ingestion dates.
    """
    try:
        registry  = load_registry()
        documents = []

        for doc_id, info in registry.items():
            documents.append(DocumentInfo(
                document_id  = doc_id,
                filename     = info["filename"],
                ingested_at  = info["ingested_at"],
            ))

        return DocumentListResponse(
            total_documents = len(documents),
            documents       = documents,
        )

    except Exception as e:
        logger.error(f"❌ Failed to list documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))