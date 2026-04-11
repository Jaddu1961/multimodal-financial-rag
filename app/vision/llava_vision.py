# ============================================
# LLAVA VISION CLIENT
# Local vision model via Ollama
# ============================================

import requests
import base64
import json
from app.utils.logger import logger


# --- Ollama API endpoint ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"
LLAVA_MODEL    = "llava"

# --- Step 1: Detection Prompt ---
DETECTION_PROMPT = """Look at this image carefully.
Does it contain any charts, graphs, bar charts, line charts, or diagrams?
Answer with only YES or NO."""

# --- Step 2: Description Prompt ---
DESCRIPTION_PROMPT = """You are analyzing a financial report image.
Describe all the charts and graphs you see in detail.
For each chart include:
- Chart type (bar, line, pie, etc.)
- What metric is shown
- Time period
- Key trends and numbers you can see

Be specific about numbers and trends."""


def encode_image_to_base64(image_path: str) -> str:
    """Encode image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def _call_llava(image_base64: str, prompt: str) -> str:
    """
    Make a single call to LLaVA via Ollama.

    Returns:
        Response text string
    """
    payload = {
        "model":  LLAVA_MODEL,
        "prompt": prompt,
        "images": [image_base64],
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 1000,
        }
    }

    response = requests.post(
        OLLAMA_API_URL,
        json    = payload,
        timeout = 120,
    )

    if response.status_code != 200:
        raise Exception(
            f"Ollama API error: {response.status_code}"
        )

    return response.json().get("response", "").strip()


def describe_image_with_llava(image_path: str) -> list[str]:
    """
    Send image to LLaVA and get graph descriptions.
    Uses 2-step approach:
    1. Detect if charts exist
    2. If yes, describe them

    Args:
        image_path: Path to PNG image

    Returns:
        List of graph description strings
    """
    # --- Encode image ---
    image_base64 = encode_image_to_base64(image_path)

    # --- Step 1: Detect charts ---
    detection = _call_llava(image_base64, DETECTION_PROMPT)
    logger.debug(f"   Detection response: {detection[:50]}")

    # --- Skip if no charts ---
    if "NO" in detection.upper() and "YES" not in detection.upper():
        return []

    # --- Step 2: Describe charts ---
    description = _call_llava(image_base64, DESCRIPTION_PROMPT)
    logger.debug(f"   Description: {description[:100]}")

    # --- Return as list if meaningful ---
    if len(description.strip()) > 30:
        return [description.strip()]

    return []


def check_ollama_running() -> bool:
    """Check if Ollama server is running."""
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        return response.status_code == 200
    except:
        return False


def check_llava_available() -> bool:
    """Check if LLaVA model is downloaded."""
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(
                "llava" in m.get("name", "")
                for m in models
            )
        return False
    except:
        return False