# ============================================
# QUERY ROUTER
# ============================================

import time
from fastapi import APIRouter, HTTPException
from app.api.schemas.query_schema import (
    QueryRequest, QueryResponse, SourceChunk,
    CompareRequest, CompareResponse,
)
from app.retrieval.qa_chain import answer_question, compare_documents
from app.utils.logger import logger


router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/ask", response_model=QueryResponse)
async def ask_question_endpoint(request: QueryRequest):
    """Ask a question about ingested financial documents."""
    start_time = time.time()
    logger.info(f"❓ Question: '{request.question[:60]}'")

    try:
        valid_types = ["text", "table", "graph", None]
        if request.filter_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail="filter_type must be: text, table, or graph"
            )

        result = answer_question(
            question    = request.question,
            n_results   = request.n_results,
            filter_type = request.filter_type,
            filter_doc  = request.filter_doc,
        )

        sources = [SourceChunk(**s) for s in result["sources"]]
        processing_time = round(time.time() - start_time, 2)

        logger.info(f"✅ Answer in {processing_time}s")

        return QueryResponse(
            success                 = True,
            question                = request.question,
            answer                  = result["answer"],
            sources                 = sources,
            types_used              = result["types_used"],
            total_chunks_used       = result["total_chunks_used"],
            processing_time_seconds = processing_time,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=CompareResponse)
async def compare_documents_endpoint(request: CompareRequest):
    """Compare the same question across two documents."""
    start_time = time.time()
    logger.info(
        f"🔄 Compare: '{request.question[:40]}' "
        f"| {request.document_1} vs {request.document_2}"
    )

    try:
        result = compare_documents(
            question   = request.question,
            document_1 = request.document_1,
            document_2 = request.document_2,
            n_results  = request.n_results,
        )

        processing_time = round(time.time() - start_time, 2)

        return CompareResponse(
            success                 = True,
            question                = request.question,
            document_1              = request.document_1,
            document_2              = request.document_2,
            answer_1                = result["answer_1"],
            answer_2                = result["answer_2"],
            combined_analysis       = result["combined_analysis"],
            processing_time_seconds = processing_time,
        )

    except Exception as e:
        logger.error(f"❌ Compare failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))