# ============================================
# GRAPH DESCRIBER
# Uses LLaVA (local) or Gemini Vision to
# describe charts and graphs in PDF pages
# ============================================

import time
from app.ingestion.image_extractor import PageImage
from app.ingestion.pdf_loader import LoadedPDF
from app.processing.document_models import DocumentChunk, ChunkType
from app.vision.llava_vision import (
    describe_image_with_llava,
    check_ollama_running,
    check_llava_available,
)
from app.utils.logger import logger
from config.settings import settings


def describe_graphs_in_pages(
    page_images: list[PageImage],
    loaded_pdf:  LoadedPDF,
) -> list[DocumentChunk]:
    """
    Analyze each page image for charts/graphs.
    Uses LLaVA (local) by default.
    Falls back to Gemini if configured.

    Args:
        page_images: List of PageImage objects
        loaded_pdf:  Original LoadedPDF for metadata

    Returns:
        List of DocumentChunk objects with type GRAPH
    """
    logger.info(f"👁️  Analyzing pages for charts: {loaded_pdf.filename}")

    # --- Check vision provider ---
    provider = settings.VISION_MODEL_PROVIDER.lower()

    if provider == "ollama":
        return _describe_with_llava(page_images, loaded_pdf)
    else:
        return _describe_with_gemini(page_images, loaded_pdf)


def _describe_with_llava(
    page_images: list[PageImage],
    loaded_pdf:  LoadedPDF,
) -> list[DocumentChunk]:
    """Use LLaVA local model for graph descriptions"""

    # --- Check Ollama is running ---
    if not check_ollama_running():
        logger.error("❌ Ollama is not running! Start it with: ollama serve")
        return []

    # --- Check LLaVA is available ---
    if not check_llava_available():
        logger.error("❌ LLaVA model not found! Download with: ollama pull llava")
        return []

    logger.info("✅ Using LLaVA (local) for graph extraction")

    chunks = []

    for page_image in page_images:
        logger.debug(
            f"   Analyzing page "
            f"{page_image.page_number}/{len(page_images)}..."
        )

        try:
            # --- Get descriptions from LLaVA ---
            descriptions = describe_image_with_llava(page_image.image_path)

            # --- Create chunks ---
            for description in descriptions:
                if len(description.strip()) < 20:
                    continue

                chunk = DocumentChunk.create(
                    text        = f"[Page {page_image.page_number}] {description}",
                    chunk_type  = ChunkType.GRAPH,
                    source_file = loaded_pdf.filename,
                    page_number = page_image.page_number,
                    document_id = loaded_pdf.document_id,
                )
                chunks.append(chunk)
                logger.debug(
                    f"   📊 Graph found on page "
                    f"{page_image.page_number}"
                )

        except Exception as e:
            logger.warning(
                f"   ⚠️  Could not analyze page "
                f"{page_image.page_number}: {e}"
            )
            continue

    logger.info(f"✅ Found {len(chunks)} graph descriptions")
    return chunks


def _describe_with_gemini(
    page_images: list[PageImage],
    loaded_pdf:  LoadedPDF,
) -> list[DocumentChunk]:
    """Use Gemini Vision API for graph descriptions"""

    try:
        import google.generativeai as genai
        from PIL import Image
        import json
        from config.model_config import GEMINI_VISION_CONFIG, VISION_PROMPT

        if not settings.GEMINI_API_KEY:
            logger.error("❌ GEMINI_API_KEY not set in .env")
            return []

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_VISION_CONFIG["model"])
        logger.info(
            f"✅ Using Gemini Vision: "
            f"{GEMINI_VISION_CONFIG['model']}"
        )

    except Exception as e:
        logger.error(f"❌ Gemini setup failed: {e}")
        return []

    chunks = []

    for page_image in page_images:
        try:
            image    = Image.open(page_image.image_path)
            response = model.generate_content(
                [VISION_PROMPT, image],
                generation_config=genai.types.GenerationConfig(
                    temperature       = GEMINI_VISION_CONFIG["temperature"],
                    max_output_tokens = GEMINI_VISION_CONFIG["max_output_tokens"],
                )
            )

            response_text = response.text.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()

            parsed = json.loads(response_text)
            graphs = parsed.get("graphs", [])

            for graph in graphs:
                if isinstance(graph, str) and len(graph.strip()) > 0:
                    chunk = DocumentChunk.create(
                        text        = f"[Page {page_image.page_number}] {graph}",
                        chunk_type  = ChunkType.GRAPH,
                        source_file = loaded_pdf.filename,
                        page_number = page_image.page_number,
                        document_id = loaded_pdf.document_id,
                    )
                    chunks.append(chunk)

            time.sleep(5)  # Rate limiting

        except Exception as e:
            logger.warning(
                f"   ⚠️  Could not analyze page "
                f"{page_image.page_number}: {e}"
            )
            continue

    logger.info(f"✅ Found {len(chunks)} graph descriptions")
    return chunks