"""
OpsPilot — Document Parser
=============================
Cleans and structures raw OCR text into manageable blocks.
"""

import re
from typing import Dict, Any

class DocumentParser:
    def __init__(self):
        pass

    def parse(self, raw_text: str) -> Dict[str, Any]:
        """
        Takes raw text and outputs a structured dictionary containing
        cleaned text, inferred title, and potential sections.
        """
        if not raw_text:
            return {"title": "Unknown Document", "content": "", "sections": []}

        # Basic cleaning
        cleaned_text = self._clean_text(raw_text)
        
        # Heuristic title extraction (assume first non-empty line is title)
        lines = [line.strip() for line in cleaned_text.split('\n') if line.strip()]
        title = lines[0] if lines else "Unknown Document"
        
        # Simple heuristic section splitting (looking for ALL CAPS lines or numbered headers)
        sections = self._extract_sections(cleaned_text)

        return {
            "title": title[:200],  # cap length
            "content": cleaned_text,
            "sections": sections,
            "char_count": len(cleaned_text),
            "word_count": len(cleaned_text.split())
        }

    def _clean_text(self, text: str) -> str:
        """Remove redundant whitespace, non-printable characters, etc."""
        # Replace multiple spaces with single space
        text = re.sub(r'[ \t]+', ' ', text)
        # Replace 3 or more newlines with double newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Remove non-printable characters except newlines and tabs
        text = re.sub(r'[^\x20-\x7E\n\t]', '', text)
        return text.strip()

    def _extract_sections(self, text: str) -> list:
        """
        Attempt to break the document into sections based on headings.
        This is a rudimentary heuristic.
        """
        sections = []
        current_header = "Introduction"
        current_content = []
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                current_content.append(line)
                continue
                
            # Heuristic for a header: short line, title cased or all caps
            if len(line) < 60 and (line.isupper() or (line.istitle() and not line.endswith('.'))):
                # Save previous section
                if current_content:
                    sections.append({
                        "header": current_header,
                        "content": "\n".join(current_content).strip()
                    })
                current_header = line
                current_content = []
            else:
                current_content.append(line)
                
        # Append last section
        if current_content:
            sections.append({
                "header": current_header,
                "content": "\n".join(current_content).strip()
            })
            
        # If no sections were found (i.e., everything fell into Introduction)
        if len(sections) == 1 and sections[0]["header"] == "Introduction" and not text.startswith("Introduction"):
            sections[0]["header"] = "Main Content"
            
        return sections
