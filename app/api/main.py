# ============================================
# FASTAPI MAIN APPLICATION
# ============================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import ingest, query, documents
from app.api.schemas.query_schema import HealthResponse
from app.vectorstore.store_manager import get_stats
from config.settings import settings
from config.model_config import EMBEDDING_CONFIG, GEMINI_LLM_CONFIG
from app.utils.logger import logger


# --- Create FastAPI app ---
app = FastAPI(
    title       = "Multimodal Financial RAG API",
    description = "RAG system for Tesla financial documents — text, tables & charts",
    version     = "1.0.0",
    docs_url    = "/docs",
    redoc_url   = "/redoc",
)

# --- CORS Middleware (for future frontend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],  # Restrict in production
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# --- Register Routers ---
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(documents.router)


# --- Health Check ---
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check system health and component status"""
    stats = get_stats()
    return HealthResponse(
        status          = "healthy",
        version         = "1.0.0",
        vector_store    = stats,
        embedding_model = EMBEDDING_CONFIG["model_name"],
        llm_model       = GEMINI_LLM_CONFIG["model"],
    )


# --- Root Endpoint ---
@app.get("/", tags=["System"])
async def root():
    return {
        "message": "🚀 Multimodal Financial RAG API is running!",
        "docs":    "/docs",
        "health":  "/health",
    }


# --- Startup Event ---
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Multimodal Financial RAG API starting...")
    logger.info(f"📚 API docs: http://localhost:{settings.API_PORT}/docs")
    logger.info(f"🔍 Health:   http://localhost:{settings.API_PORT}/health")