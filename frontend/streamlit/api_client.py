# ============================================
# API CLIENT
# Handles all FastAPI backend communication
# ============================================

import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.streamlit.config import API_ENDPOINTS


def check_health() -> dict:
    """
    Check if backend API is running.

    Returns:
        Dict with health status or error
    """
    try:
        response = requests.get(
            API_ENDPOINTS["health"],
            timeout=5
        )
        if response.status_code == 200:
            return {"status": "online", "data": response.json()}
        return {"status": "error", "data": None}

    except requests.exceptions.ConnectionError:
        return {"status": "offline", "data": None}
    except Exception as e:
        return {"status": "error", "data": str(e)}


def ask_question(
    question:    str,
    n_results:   int  = 5,
    filter_type: str  = None,
) -> dict:
    """
    Send question to RAG backend and get answer.

    Args:
        question:    User's question
        n_results:   Number of chunks to retrieve
        filter_type: Optional filter (text/table/graph)

    Returns:
        Dict with answer, sources, metadata
    """
    try:
        payload = {
            "question":    question,
            "n_results":   n_results,
            "filter_type": filter_type,
        }

        response = requests.post(
            API_ENDPOINTS["query"],
            json    = payload,
            timeout = 30,
        )

        if response.status_code == 200:
            return {"success": True, "data": response.json()}

        return {
            "success": False,
            "error":   f"API Error {response.status_code}: {response.text}"
        }

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to backend. Is the server running?"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_documents() -> dict:
    """
    Get list of ingested documents.

    Returns:
        Dict with documents list
    """
    try:
        response = requests.get(
            API_ENDPOINTS["documents"],
            timeout=10
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "error": response.text}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_stats() -> dict:
    """
    Get vector store statistics.

    Returns:
        Dict with stats
    """
    try:
        response = requests.get(
            API_ENDPOINTS["stats"],
            timeout=10
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        return {"success": False, "error": response.text}

    except Exception as e:
        return {"success": False, "error": str(e)}