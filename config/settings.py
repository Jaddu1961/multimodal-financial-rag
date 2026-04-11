# ============================================
# SETTINGS - Reads from .env automatically
# ============================================

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):

    # --- Project Root ---
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # --- Gemini API ---
    GEMINI_API_KEY: str = ""

    # --- Groq API ---
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-70b-8192"

    # --- Model Providers ---
    VISION_MODEL_PROVIDER: str = "gemini"   # "gemini" or "ollama"
    LLM_PROVIDER: str = "gemini"            # "gemini" or "ollama"

    # --- Gemini Model Names ---
    GEMINI_LLM_MODEL: str = "gemini-1.5-flash"
    GEMINI_VISION_MODEL: str = "gemini-1.5-flash"

    # --- Ollama Settings ---
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_LLM_MODEL: str = "llama3"
    OLLAMA_VISION_MODEL: str = "llava"

    # --- Embedding Settings ---
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DEVICE: str = "cpu"

    # --- ChromaDB Settings ---
    CHROMA_PERSIST_PATH: str = "./vectorstore_data/chroma"
    CHROMA_COLLECTION_NAME: str = "financial_rag"

    # --- Ingestion Settings ---
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_CHUNK_SIZE: int = 4000
    IMAGE_DPI: int = 200

    # --- Retrieval Settings ---
    TOP_K_RESULTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7

    # --- API Settings ---
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG_MODE: bool = True

    # --- Data Paths ---
    RAW_DATA_PATH: str = "./data/raw"
    PROCESSED_DATA_PATH: str = "./data/processed"
    IMAGES_PATH: str = "./data/images"
    LOGS_PATH: str = "./logs"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# ---- Single instance used across entire app ----
settings = Settings()