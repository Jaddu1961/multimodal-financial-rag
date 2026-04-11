# ============================================
# QUERY ROUTER
# Handles question answering
# ============================================

import time
from fastapi import APIRouter, HTTPException
from app.api.schemas.query_schema import QueryRequest, QueryResponse, SourceChunk
from app.retrieval.qa_chain import answer_question
from app.utils.logger import logger


router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Ask a question about the ingested financial documents.

    The system will:
    1. Embed your question
    2. Find relevant chunks (text, tables, graphs)
    3. Generate a grounded answer using Gemini
    4. Return the answer with source citations
    """
    start_time = time.time()

    logger.info(f"❓ Question received: '{request.question[:60]}'")

    try:
        # --- Validate filter_type ---
        valid_types = ["text", "table", "graph", None]
        if request.filter_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"filter_type must be one of: text, table, graph"
            )

        # --- Generate answer ---
        result = answer_question(
            question    = request.question,
            n_results   = request.n_results,
            filter_type = request.filter_type,
            filter_doc  = request.filter_doc,
        )

        # --- Format sources ---
        sources = [SourceChunk(**s) for s in result["sources"]]

        processing_time = round(time.time() - start_time, 2)

        logger.info(f"✅ Answer generated in {processing_time}s")

        return QueryResponse(
            success             = True,
            question            = request.question,
            answer              = result["answer"],
            sources             = sources,
            types_used          = result["types_used"],
            total_chunks_used   = result["total_chunks_used"],
            processing_time_seconds = processing_time,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))