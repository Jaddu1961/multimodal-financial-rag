# ============================================
# DOCUMENT MODELS
# Defines data structures for all chunk types
# ============================================

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import hashlib
import time


class ChunkType(str, Enum):
    """Types of content chunks in the system"""
    TEXT  = "text"
    TABLE = "table"
    GRAPH = "graph"


class DocumentChunk(BaseModel):
    """
    Represents a single chunk of content extracted from a PDF.
    This is the core data structure used throughout the entire pipeline.
    """

    # --- Identity ---
    chunk_id:        str       = Field(..., description="Unique identifier for this chunk")
    document_id:     str       = Field(..., description="ID of the source document")

    # --- Content ---
    text:            str       = Field(..., description="Text content of the chunk")
    chunk_type:      ChunkType = Field(..., description="Type: text, table, or graph")

    # --- Source Metadata ---
    source_file:     str       = Field(..., description="Original PDF filename")
    page_number:     int       = Field(..., description="Page number in the PDF")

    # --- Optional Metadata ---
    fiscal_quarter:  Optional[str] = Field(None, description="e.g. Q3-2023")
    section:         Optional[str] = Field(None, description="Section of the document")

    # --- Timestamps ---
    created_at:      float     = Field(default_factory=time.time)

    @classmethod
    def create(
        cls,
        text:           str,
        chunk_type:     ChunkType,
        source_file:    str,
        page_number:    int,
        document_id:    str,
        fiscal_quarter: Optional[str] = None,
        section:        Optional[str] = None,
    ) -> "DocumentChunk":
        """
        Factory method to create a chunk with auto-generated ID.
        ID is based on content hash so duplicates are detectable.
        """
        chunk_id = hashlib.md5(
            f"{source_file}_{page_number}_{chunk_type}_{text[:100]}".encode()
        ).hexdigest()

        return cls(
            chunk_id       = chunk_id,
            document_id    = document_id,
            text           = text,
            chunk_type     = chunk_type,
            source_file    = source_file,
            page_number    = page_number,
            fiscal_quarter = fiscal_quarter,
            section        = section,
        )

    def to_metadata(self) -> dict:
        """
        Returns metadata dict for storing in ChromaDB.
        ChromaDB only accepts str, int, float, bool values.
        """
        return {
            "chunk_id":       self.chunk_id,
            "document_id":    self.document_id,
            "chunk_type":     self.chunk_type.value,
            "source_file":    self.source_file,
            "page_number":    self.page_number,
            "fiscal_quarter": self.fiscal_quarter or "",
            "section":        self.section or "",
            "created_at":     self.created_at,
        }


class Document(BaseModel):
    """
    Represents a full ingested PDF document
    with all its extracted chunks.
    """
    document_id:    str              = Field(..., description="Unique document identifier")
    filename:       str              = Field(..., description="PDF filename")
    file_path:      str              = Field(..., description="Full path to the PDF")
    total_pages:    int              = Field(..., description="Total pages in the PDF")
    fiscal_quarter: Optional[str]   = Field(None, description="e.g. Q3-2023")
    chunks:         list[DocumentChunk] = Field(default_factory=list)
    created_at:     float            = Field(default_factory=time.time)

    @property
    def total_chunks(self) -> int:
        return len(self.chunks)

    @property
    def text_chunks(self) -> list[DocumentChunk]:
        return [c for c in self.chunks if c.chunk_type == ChunkType.TEXT]

    @property
    def table_chunks(self) -> list[DocumentChunk]:
        return [c for c in self.chunks if c.chunk_type == ChunkType.TABLE]

    @property
    def graph_chunks(self) -> list[DocumentChunk]:
        return [c for c in self.chunks if c.chunk_type == ChunkType.GRAPH]

    def summary(self) -> dict:
        """Returns a summary of the document for logging/API responses"""
        return {
            "document_id":    self.document_id,
            "filename":       self.filename,
            "total_pages":    self.total_pages,
            "total_chunks":   self.total_chunks,
            "text_chunks":    len(self.text_chunks),
            "table_chunks":   len(self.table_chunks),
            "graph_chunks":   len(self.graph_chunks),
            "fiscal_quarter": self.fiscal_quarter,
        }