# ============================================
# PDF LOADER
# Loads and validates PDF files
# ============================================

import fitz  # PyMuPDF
import hashlib
from pathlib import Path
from dataclasses import dataclass
from app.utils.logger import logger


@dataclass
class PDFPage:
    """Represents a single page from a PDF"""
    page_number:  int
    text:         str
    width:        float
    height:       float
    has_images:   bool


@dataclass
class LoadedPDF:
    """Represents a fully loaded PDF document"""
    file_path:    str
    filename:     str
    document_id:  str
    total_pages:  int
    pages:        list[PDFPage]


def load_pdf(file_path: str) -> LoadedPDF:
    """
    Load a PDF file and extract basic info from each page.

    Args:
        file_path: Path to the PDF file

    Returns:
        LoadedPDF object with all pages

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not a valid PDF
    """
    path = Path(file_path)

    # --- Validate file ---
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"File is not a PDF: {file_path}")

    logger.info(f"📄 Loading PDF: {path.name}")

    # --- Generate document ID from file hash ---
    document_id = _generate_document_id(file_path)

    # --- Open PDF with PyMuPDF ---
    pdf_document = fitz.open(file_path)
    total_pages  = len(pdf_document)

    logger.info(f"📖 Total pages: {total_pages}")

    # --- Extract each page ---
    pages = []
    for page_num in range(total_pages):
        page     = pdf_document[page_num]
        text     = page.get_text("text")
        images   = page.get_images()
        rect     = page.rect

        pdf_page = PDFPage(
            page_number = page_num + 1,  # 1-indexed
            text        = text.strip(),
            width       = rect.width,
            height      = rect.height,
            has_images  = len(images) > 0,
        )
        pages.append(pdf_page)

    pdf_document.close()

    logger.info(f"✅ PDF loaded successfully: {path.name}")
    logger.info(f"   Pages with images: {sum(1 for p in pages if p.has_images)}")

    return LoadedPDF(
        file_path   = str(file_path),
        filename    = path.name,
        document_id = document_id,
        total_pages = total_pages,
        pages       = pages,
    )


def _generate_document_id(file_path: str) -> str:
    """Generate unique document ID from file content hash"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()