# ============================================
# IMAGE EXTRACTOR
# Converts PDF pages to images for vision AI
# ============================================

import fitz  # PyMuPDF
from pathlib import Path
from dataclasses import dataclass
from app.ingestion.pdf_loader import LoadedPDF
from app.utils.logger import logger
from config.settings import settings


@dataclass
class PageImage:
    """Represents a single PDF page converted to image"""
    page_number: int
    image_path:  str
    width:       int
    height:      int
    has_images:  bool  # Whether page had embedded images


def extract_page_images(
    loaded_pdf:  LoadedPDF,
    output_dir:  str = None,
    dpi:         int = None,
) -> list[PageImage]:
    """
    Convert each PDF page to a PNG image.

    Args:
        loaded_pdf:  LoadedPDF object
        output_dir:  Where to save images (default: data/images)
        dpi:         Resolution for conversion (default from settings)

    Returns:
        List of PageImage objects
    """
    # --- Setup output directory ---
    if output_dir is None:
        output_dir = settings.IMAGES_PATH

    if dpi is None:
        dpi = settings.IMAGE_DPI

    # Create subfolder per document
    doc_folder = Path(output_dir) / loaded_pdf.document_id
    doc_folder.mkdir(parents=True, exist_ok=True)

    logger.info(f"🖼️  Converting PDF pages to images: {loaded_pdf.filename}")
    logger.info(f"   DPI: {dpi} | Output: {doc_folder}")

    page_images = []
    pdf_doc     = fitz.open(loaded_pdf.file_path)

    for page_num in range(loaded_pdf.total_pages):
        page = pdf_doc[page_num]

        # --- Convert page to image ---
        # Matrix controls the resolution (DPI)
        zoom   = dpi / 72  # 72 is default PDF DPI
        matrix = fitz.Matrix(zoom, zoom)
        pixmap = page.get_pixmap(matrix=matrix)

        # --- Save as PNG ---
        image_filename = f"page_{page_num + 1:03d}.png"
        image_path     = doc_folder / image_filename
        pixmap.save(str(image_path))

        page_image = PageImage(
            page_number = page_num + 1,
            image_path  = str(image_path),
            width       = pixmap.width,
            height      = pixmap.height,
            has_images  = loaded_pdf.pages[page_num].has_images,
        )
        page_images.append(page_image)

        logger.debug(f"   ✅ Page {page_num + 1}/{loaded_pdf.total_pages} → {image_filename}")

    pdf_doc.close()

    logger.info(f"✅ Converted {len(page_images)} pages to images")
    return page_images


def cleanup_images(document_id: str, output_dir: str = None) -> None:
    """
    Delete all images for a document after processing.
    Saves disk space.

    Args:
        document_id: Document ID (subfolder name)
        output_dir:  Base images directory
    """
    import shutil

    if output_dir is None:
        output_dir = settings.IMAGES_PATH

    doc_folder = Path(output_dir) / document_id

    if doc_folder.exists():
        shutil.rmtree(doc_folder)
        logger.info(f"🗑️  Cleaned up images for document: {document_id}")