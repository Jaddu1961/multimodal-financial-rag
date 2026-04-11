# ============================================
# TEXT EXTRACTOR
# Extracts text and tables from PDF pages
# ============================================

import fitz  # PyMuPDF
from pathlib import Path
from app.ingestion.pdf_loader import LoadedPDF
from app.processing.document_models import DocumentChunk, ChunkType
from app.utils.logger import logger
from config.settings import settings


def extract_text_chunks(loaded_pdf: LoadedPDF) -> list[DocumentChunk]:
    """
    Extract text chunks from all pages of a loaded PDF.

    Args:
        loaded_pdf: LoadedPDF object from pdf_loader

    Returns:
        List of DocumentChunk objects with type TEXT
    """
    logger.info(f"📝 Extracting text from: {loaded_pdf.filename}")

    chunks = []

    for page in loaded_pdf.pages:
        # Skip empty pages
        if not page.text or len(page.text.strip()) < 50:
            logger.debug(f"   Skipping empty page {page.page_number}")
            continue

        # Split page text into smaller chunks
        page_chunks = _split_text_into_chunks(
            text        = page.text,
            chunk_size  = settings.CHUNK_SIZE,
            overlap     = settings.CHUNK_OVERLAP,
        )

        for chunk_text in page_chunks:
            if len(chunk_text.strip()) < 50:
                continue

            chunk = DocumentChunk.create(
                text        = chunk_text.strip(),
                chunk_type  = ChunkType.TEXT,
                source_file = loaded_pdf.filename,
                page_number = page.page_number,
                document_id = loaded_pdf.document_id,
            )
            chunks.append(chunk)

    logger.info(f"✅ Extracted {len(chunks)} text chunks")
    return chunks


def extract_table_chunks(loaded_pdf: LoadedPDF) -> list[DocumentChunk]:
    """
    Extract table data from PDF using PyMuPDF.

    Args:
        loaded_pdf: LoadedPDF object from pdf_loader

    Returns:
        List of DocumentChunk objects with type TABLE
    """
    logger.info(f"📊 Extracting tables from: {loaded_pdf.filename}")

    chunks  = []
    pdf_doc = fitz.open(loaded_pdf.file_path)

    for page_num, page in enumerate(loaded_pdf.pages):
        fitz_page = pdf_doc[page_num]

        # --- Find tables on this page ---
        try:
            tabs = fitz_page.find_tables()
            if not tabs or not tabs.tables:
                continue

            for table in tabs.tables:
                table_data = table.extract()

                if not table_data:
                    continue

                # Convert table to readable text format
                table_text = _table_to_text(table_data)

                if len(table_text.strip()) < 20:
                    continue

                chunk = DocumentChunk.create(
                    text        = table_text,
                    chunk_type  = ChunkType.TABLE,
                    source_file = loaded_pdf.filename,
                    page_number = page.page_number,
                    document_id = loaded_pdf.document_id,
                )
                chunks.append(chunk)

        except Exception as e:
            logger.warning(f"   Could not extract table on page {page.page_number}: {e}")
            continue

    pdf_doc.close()
    logger.info(f"✅ Extracted {len(chunks)} table chunks")
    return chunks


def _split_text_into_chunks(
    text:       str,
    chunk_size: int,
    overlap:    int,
) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text:       Full text to split
        chunk_size: Maximum characters per chunk
        overlap:    Overlapping characters between chunks

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start  = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at a sentence or newline
        if end < len(text):
            # Look for good break point
            for break_char in ["\n\n", "\n", ". ", " "]:
                break_point = text.rfind(break_char, start, end)
                if break_point > start:
                    end = break_point + len(break_char)
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move forward with overlap
        start = end - overlap
        if start <= 0 or start >= len(text):
            break

    return chunks


def _table_to_text(table_data: list[list]) -> str:
    """
    Convert table data (list of rows) to readable text.

    Example output:
    Header1 | Header2 | Header3
    Value1  | Value2  | Value3
    """
    if not table_data:
        return ""

    lines = []
    for row in table_data:
        # Clean None values
        cleaned = [str(cell).strip() if cell else "" for cell in row]
        line    = " | ".join(cleaned)
        lines.append(line)

    return "\n".join(lines)