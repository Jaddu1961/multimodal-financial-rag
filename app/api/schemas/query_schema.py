# ============================================
# QUERY SCHEMAS
# Request/Response models for query API
# ============================================

from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    """Request body for asking a question"""
    question:    str         = Field(..., min_length=5, description="Question to ask")
    n_results:   int         = Field(default=5, ge=1, le=20)
    filter_type: Optional[str] = Field(
        default=None,
        description="Filter by chunk type: 'text', 'table', or 'graph'"
    )
    filter_doc:  Optional[str] = Field(
        default=None,
        description="Filter by document ID"
    )


class SourceChunk(BaseModel):
    """A single source chunk used to answer the question"""
    chunk_type:  str
    page_number: int
    source_file: str
    relevance:   float
    preview:     str


class QueryResponse(BaseModel):
    """Response returned after answering a question"""
    success:            bool
    question:           str
    answer:             str
    sources:            list[SourceChunk]
    types_used:         dict
    total_chunks_used:  int
    processing_time_seconds: float


class HealthResponse(BaseModel):
    """Response for health check endpoint"""
    status:          str
    version:         str
    vector_store:    dict
    embedding_model: str
    llm_model:       str