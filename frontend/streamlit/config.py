# ============================================
# FRONTEND CONFIGURATION
# ============================================

# --- API Settings ---
API_BASE_URL = "http://localhost:8000"

API_ENDPOINTS = {
    "health":    f"{API_BASE_URL}/health",
    "query":     f"{API_BASE_URL}/query/ask",
    "ingest":    f"{API_BASE_URL}/ingest/upload",
    "documents": f"{API_BASE_URL}/documents/list",
    "stats":     f"{API_BASE_URL}/ingest/stats",
}

# --- App Settings ---
APP_TITLE       = "Tesla Financial Intelligence"
APP_SUBTITLE    = "Powered by Multimodal RAG"
APP_ICON        = "🚗"
APP_VERSION     = "1.0.0"

# --- Chat Settings ---
MAX_HISTORY     = 20
DEFAULT_N_RESULTS = 5

# --- Theme Colors ---
COLORS = {
    "primary":      "#2563EB",   # Tesla Red
    "secondary":    "#1A1A1A",   # Dark
    "background":   "#0D0D0D",   # Near Black
    "surface":      "#1E1E1E",   # Card Background
    "text":         "#FFFFFF",   # White
    "text_muted":   "#888888",   # Gray
    "success":      "#00C853",   # Green
    "warning":      "#FFB300",   # Amber
    "border":       "#333333",   # Border
}

# --- Source Type Config ---
SOURCE_ICONS = {
    "text":  "📝",
    "table": "📊",
    "graph": "📈",
}

SOURCE_COLORS = {
    "text":  "#4A90D9",
    "table": "#7B68EE",
    "graph": "#50C878",
}

# --- Sample Questions ---
SAMPLE_QUESTIONS = [
    "What was Tesla's total revenue in Q3 2023?",
    "What is Tesla's gross profit margin?",
    "How did operating expenses change in Q3 2023?",
    "What are Tesla's vehicle delivery numbers?",
    "How did Tesla's energy business perform?",
    "What is Tesla's free cash flow in Q3 2023?",
]