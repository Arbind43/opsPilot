"""
OpsPilot — OCR Engine
========================
Extracts raw text from PDFs, Images, and Text files.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class OCREngine:
    def __init__(self):
        # Initialize Tesseract, PyMuPDF, etc. if available.
        # In a real environment, you'd load models here.
        pass

    def extract_text(self, file_path: str, file_type: str) -> str:
        """
        Extract text from the given file based on its type.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            return self._extract_from_pdf(file_path)
        elif ext in ['.png', '.jpg', '.jpeg']:
            return self._extract_from_image(file_path)
        elif ext in ['.txt', '.md', '.csv']:
            return self._extract_from_text(file_path)
        elif ext in ['.docx']:
            return self._extract_from_docx(file_path)
        else:
            logger.warning(f"Unsupported file type for OCR: {ext}")
            return f"[Unsupported file type: {ext}]"

    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using PyMuPDF (fitz) or pdfplumber."""
        text = ""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text("text") + "\n"
            doc.close()
        except ImportError:
            logger.warning("PyMuPDF (fitz) not installed. Falling back to stub extraction.")
            text = f"[PDF Text Extraction Stub for {os.path.basename(file_path)}]\n"
            # Fallback logic here if needed (e.g. PyPDF2)
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}")
            raise
            
        return text.strip()

    def _extract_from_image(self, file_path: str) -> str:
        """Extract text from images using Gemini Vision for P&ID intelligence."""
        import base64
        from langchain_core.messages import HumanMessage
        from ai.llm_factory import get_llm

        try:
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            
            ext = os.path.splitext(file_path)[1].lower().replace('.', '')
            if ext == 'jpg': ext = 'jpeg'
            
            llm = get_llm(temperature=0.1)
            message = HumanMessage(
                content=[
                    {
                        "type": "text", 
                        "text": "You are an expert industrial engineer. Extract all readable text from this document. If this is a P&ID, schematic, or diagram, carefully describe the visual components (valves, pumps, tanks, pipes) and their connections. Output the information clearly as plain text."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/{ext};base64,{encoded_string}"}
                    }
                ]
            )
            logger.info(f"Sending image {os.path.basename(file_path)} to Gemini Vision API")
            res = llm.invoke([message])
            return str(res.content).strip()
        except Exception as e:
            logger.error(f"Error extracting Image with Gemini: {e}")
            return f"[Image AI Extraction Failed: {str(e)}]"

    def _extract_from_text(self, file_path: str) -> str:
        """Read raw text."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback for different encodings
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()

    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX using python-docx."""
        try:
            import docx
            doc = docx.Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except ImportError:
            logger.warning("python-docx not installed. Falling back to stub extraction.")
            return f"[DOCX Extraction Stub for {os.path.basename(file_path)}]\n"
