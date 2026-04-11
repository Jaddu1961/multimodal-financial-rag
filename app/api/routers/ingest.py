# ============================================
# INGEST ROUTER
# Handles PDF upload and processing
# ============================================

import time
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.api.schemas.ingest_schema import (
    IngestResponse,
    DeleteResponse,
    StatsResponse,
)
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.text_extractor import extract_text_chunks, extract_table_chunks
from app.ingestion.image_extractor import extract_page_images, cleanup_images
from app.ingestion.graph_describer import describe_graphs_in_pages
from app.vectorstore.store_manager import store_chunks, get_stats, remove_document
from app.processing.deduplicator import is_duplicate, register_document
from app.utils.logger import logger
from config.settings import settings


router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/upload", response_model=IngestResponse)
async def ingest_document(
    file:          UploadFile = File(...),
    extract_graphs: bool      = Query(default=True,  description="Extract graph descriptions"),
    skip_duplicates: bool     = Query(default=True,  description="Skip already ingested docs"),
    fiscal_quarter: str       = Query(default=None,  description="e.g. Q3-2023"),
):
    """
    Upload and ingest a PDF financial document.

    This endpoint:
    1. Saves the uploaded PDF
    2. Extracts text and table chunks
    3. Optionally extracts graph descriptions using Vision AI
    4. Embeds all chunks and stores in ChromaDB
    """
    start_time = time.time()

    # --- Validate file type ---
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # --- Save uploaded file ---
    raw_dir   = Path(settings.RAW_DATA_PATH)
    raw_dir.mkdir(parents=True, exist_ok=True)
    file_path = raw_dir / file.filename

    logger.info(f"📤 Received upload: {file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # --- Load PDF ---
        loaded_pdf = load_pdf(str(file_path))

        # --- Check for duplicates ---
        if skip_duplicates and is_duplicate(loaded_pdf.document_id, loaded_pdf.filename):
            return IngestResponse(
                success        = False,
                message        = f"Document already ingested: {file.filename}",
                document_id    = loaded_pdf.document_id,
                filename       = loaded_pdf.filename,
                total_pages    = loaded_pdf.total_pages,
                chunks_stored  = 0,
                text_chunks    = 0,
                table_chunks   = 0,
                graph_chunks   = 0,
                processing_time_seconds = round(time.time() - start_time, 2),
            )

        # --- Extract text chunks ---
        text_chunks  = extract_text_chunks(loaded_pdf)

        # --- Extract table chunks ---
        table_chunks = extract_table_chunks(loaded_pdf)

        # --- Extract graph descriptions (optional) ---
        graph_chunks = []
        if extract_graphs:
            try:
                page_images  = extract_page_images(loaded_pdf)
                graph_chunks = describe_graphs_in_pages(page_images, loaded_pdf)
                cleanup_images(loaded_pdf.document_id)
            except Exception as e:
                logger.warning(f"⚠️  Graph extraction failed: {e}. Continuing without graphs.")

        # --- Combine all chunks ---
        all_chunks = text_chunks + table_chunks + graph_chunks

        if not all_chunks:
            raise HTTPException(
                status_code=422,
                detail="No content could be extracted from the PDF"
            )

        # --- Store in ChromaDB ---
        store_result = store_chunks(all_chunks)

        # --- Register as ingested ---
        register_document(loaded_pdf.document_id, loaded_pdf.filename)

        processing_time = round(time.time() - start_time, 2)

        logger.info(
            f"✅ Ingestion complete: {file.filename} "
            f"({len(all_chunks)} chunks in {processing_time}s)"
        )

        return IngestResponse(
            success        = True,
            message        = f"Successfully ingested: {file.filename}",
            document_id    = loaded_pdf.document_id,
            filename       = loaded_pdf.filename,
            total_pages    = loaded_pdf.total_pages,
            chunks_stored  = store_result["stored"],
            text_chunks    = len(text_chunks),
            table_chunks   = len(table_chunks),
            graph_chunks   = len(graph_chunks),
            processing_time_seconds = processing_time,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/document/{document_id}", response_model=DeleteResponse)
async def delete_document(document_id: str):
    """Delete all chunks for a specific document"""
    try:
        remove_document(document_id)
        return DeleteResponse(
            success     = True,
            message     = f"Document deleted: {document_id}",
            document_id = document_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatsResponse)
async def get_vector_store_stats():
    """Get current vector store statistics"""
    stats = get_stats()
    return StatsResponse(**stats)