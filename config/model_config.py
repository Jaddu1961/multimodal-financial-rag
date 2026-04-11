# ============================================
# MODEL CONFIGURATION
# ============================================

from config.settings import settings


# --- Embedding Model Config ---
EMBEDDING_CONFIG = {
    "model_name": settings.EMBEDDING_MODEL,
    "device": settings.EMBEDDING_DEVICE,
    "batch_size": 32,
    "normalize_embeddings": True,
}


# --- Gemini LLM Config ---
GEMINI_LLM_CONFIG = {
    "model": settings.GEMINI_LLM_MODEL,
    "temperature": 0.2,       # Low = more factual answers
    "max_output_tokens": 2048,
    "top_p": 0.8,
    "top_k": 40,
}


# --- Gemini Vision Config ---
GEMINI_VISION_CONFIG = {
    "model": settings.GEMINI_VISION_MODEL,
    "temperature": 0.1,       # Very low = consistent descriptions
    "max_output_tokens": 1000,
}
# --- Groq LLM Config ---
GROQ_LLM_CONFIG = {
    "model": settings.GROQ_MODEL,
    "temperature": 0.2,
    "max_tokens": 2048,
}


# --- Ollama LLM Config ---
OLLAMA_LLM_CONFIG = {
    "model": settings.OLLAMA_LLM_MODEL,
    "base_url": settings.OLLAMA_BASE_URL,
    "temperature": 0.2,
    "num_predict": 2048,
}


# --- Ollama Vision Config ---
OLLAMA_VISION_CONFIG = {
    "model": settings.OLLAMA_VISION_MODEL,
    "base_url": settings.OLLAMA_BASE_URL,
    "temperature": 0.1,
    "num_predict": 1000,
}


# --- ChromaDB Config ---
CHROMA_CONFIG = {
    "persist_directory": settings.CHROMA_PERSIST_PATH,
    "collection_name": settings.CHROMA_COLLECTION_NAME,
    "distance_metric": "cosine",  # Best for semantic similarity
}


# --- Chunking Config ---
CHUNKING_CONFIG = {
    "chunk_size": settings.CHUNK_SIZE,
    "chunk_overlap": settings.CHUNK_OVERLAP,
    "max_chunk_size": settings.MAX_CHUNK_SIZE,
    "separators": ["\n\n", "\n", ". ", " ", ""],
}


# --- Vision Prompt Config ---
VISION_PROMPT = """You are a financial analyst assistant specialized in 
reading charts and graphs from financial reports.

Analyze the image and identify any charts, graphs, or diagrams.

For each chart found, describe:
1. Chart type (bar, line, pie, etc.)
2. What metric is being shown
3. Time period covered
4. Key trends or patterns
5. Notable data points or anomalies

Return your response in this exact JSON format:
{
  "graphs": [
    "Description of chart 1...",
    "Description of chart 2..."
  ]
}

If no charts are found, return: {"graphs": []}

Do not include any text outside the JSON. Be concise but specific."""


# --- RAG Prompt Config ---
RAG_SYSTEM_PROMPT = """You are a financial analyst assistant helping users 
understand Tesla's financial reports.

You will be given relevant context retrieved from Tesla's financial documents,
which may include text excerpts, table data, and chart descriptions.

Instructions:
- Answer ONLY based on the provided context
- If the context does not contain enough information, say so clearly
- Always mention which type of source supports your answer 
  (text, table, or chart description)
- Be precise with numbers and dates
- Do not make up or infer data not present in the context"""


RAG_USER_PROMPT_TEMPLATE = """Context from Tesla Financial Documents:
{context}

User Question: {question}

Please provide a detailed answer based strictly on the context above."""