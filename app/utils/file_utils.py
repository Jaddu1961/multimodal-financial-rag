# ============================================
# FILE UTILITIES
# ============================================

import hashlib
from pathlib import Path
from app.utils.logger import logger


def get_file_hash(file_path: str) -> str:
    """
    Generate MD5 hash of a file.
    Used to detect duplicate documents.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def ensure_directory(path: str) -> Path:
    """
    Create directory if it doesn't exist.
    Returns Path object.
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_filename_without_extension(file_path: str) -> str:
    """Returns filename without extension"""
    return Path(file_path).stem


def validate_pdf(file_path: str) -> bool:
    """
    Check if file exists and is a PDF.
    Returns True if valid, False otherwise.
    """
    path = Path(file_path)

    if not path.exists():
        logger.error(f"File not found: {file_path}")
        return False

    if path.suffix.lower() != ".pdf":
        logger.error(f"File is not a PDF: {file_path}")
        return False

    if path.stat().st_size == 0:
        logger.error(f"File is empty: {file_path}")
        return False

    logger.info(f"✅ Valid PDF: {file_path}")
    return True