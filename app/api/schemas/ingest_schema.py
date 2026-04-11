# ============================================
# INGEST SCHEMAS
# Request/Response models for ingestion API
# ============================================

from pydantic import BaseModel
from typing import Optional


class IngestResponse(BaseModel):
    """Response returned after ingesting a document"""
    success:        bool
    message:        str
    document_id:    str
    filename:       str
    total_pages:    int
    chunks_stored:  int
    text_chunks:    int
    table_chunks:   int
    graph_chunks:   int
    processing_time_seconds: float


class DocumentInfo(BaseModel):
    """Info about a single ingested document"""
    document_id:    str
    filename:       str
    ingested_at:    str


class DocumentListResponse(BaseModel):
    """Response for listing all ingested documents"""
    total_documents: int
    documents:       list[DocumentInfo]


class DeleteResponse(BaseModel):
    """Response after deleting a document"""
    success:     bool
    message:     str
    document_id: str


class StatsResponse(BaseModel):
    """Response for vector store statistics"""
    collection_name: str
    total_chunks:    int
    persist_path:    str