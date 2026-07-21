"""
OpsPilot — File Utilities
===========================
Helper functions for file handling and validations.
"""

import os
import uuid
import mimetypes

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.xlsx', '.csv', '.txt', '.png', '.jpg', '.jpeg'}

def validate_file_extension(filename: str) -> bool:
    """Check if the file extension is allowed."""
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def generate_storage_path(base_dir: str, filename: str) -> str:
    """Generate a unique secure file path."""
    ext = os.path.splitext(filename)[1].lower()
    unique_name = f"{uuid.uuid4()}{ext}"
    return os.path.join(base_dir, unique_name)

def get_file_type(filename: str) -> str:
    """Map extension to general document category."""
    ext = os.path.splitext(filename)[1].lower()
    if ext in {'.pdf'}:
        return "manual"
    elif ext in {'.docx', '.txt'}:
        return "report"
    elif ext in {'.xlsx', '.csv'}:
        return "data"
    elif ext in {'.png', '.jpg', '.jpeg'}:
        return "schematic"
    return "other"
