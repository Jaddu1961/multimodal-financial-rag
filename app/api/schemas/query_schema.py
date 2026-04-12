# ============================================
# QUERY SCHEMAS
# ============================================

from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    """Request body for asking a question"""
    question:    str         = Field(..., min_length=5)
    n_results:   int         = Field(default=8, ge=1, le=20)
    filter_type: Optional[str] = Field(default=None)
    filter_doc:  Optional[str] = Field(default=None)


class CompareRequest(BaseModel):
    """Request body for comparing two documents"""
    question:   str = Field(..., min_length=5)
    document_1: str = Field(..., description="First document filename")
    document_2: str = Field(..., description="Second document filename")
    n_results:  int = Field(default=5, ge=1, le=10)


class SourceChunk(BaseModel):
    """A single source chunk"""
    chunk_type:  str
    page_number: int
    source_file: str
    relevance:   float
    preview:     str


class QueryResponse(BaseModel):
    """Response for single question"""
    success:                 bool
    question:                str
    answer:                  str
    sources:                 list[SourceChunk]
    types_used:              dict
    total_chunks_used:       int
    processing_time_seconds: float


class CompareResponse(BaseModel):
    """Response for comparison question"""
    success:                 bool
    question:                str
    document_1:              str
    document_2:              str
    answer_1:                str
    answer_2:                str
    combined_analysis:       str
    processing_time_seconds: float


class HealthResponse(BaseModel):
    """Response for health check"""
    status:          str
    version:         str
    vector_store:    dict
    embedding_model: str
    llm_model:       str