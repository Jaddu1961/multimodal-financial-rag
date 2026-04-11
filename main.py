# ============================================
# MAIN ENTRY POINT
# ============================================

import uvicorn
from config.settings import settings
from config.logging_config import setup_logging

# Setup logging first
logger = setup_logging()


if __name__ == "__main__":
    logger.info("🚀 Starting Multimodal Financial RAG System...")
    logger.info(f"🌐 API running at http://{settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"📚 Docs available at http://localhost:{settings.API_PORT}/docs")

    uvicorn.run(
        "app.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG_MODE,
        log_level="debug" if settings.DEBUG_MODE else "info",
    )