import re
from typing import Dict, Any, Optional
from ..models.document import Document
from .base_processor import BaseProcessor


class TextProcessor(BaseProcessor):
    """Processor for cleaning and normalizing extracted text."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the text processor with configuration.
        
        Args:
            config: Configuration dictionary that may include:
                - remove_extra_whitespace: Remove extra whitespace (default: True)
                - fix_line_breaks: Fix broken line breaks (default: True)
                - remove_headers_footers: Attempt to remove headers/footers (default: False)
                - normalize_characters: Normalize special characters (default: True)
        """
        super().__init__(config)
        self.remove_extra_whitespace = self.config.get('remove_extra_whitespace', True)
        self.fix_line_breaks = self.config.get('fix_line_breaks', True)
        self.remove_headers_footers = self.config.get('remove_headers_footers', False)
        self.normalize_characters = self.config.get('normalize_characters', True)
    
    def process(self, document: Document) -> Document:
        """
        Clean and normalize the text in the document.
        
        Args:
            document: Document object with extracted text
            
        Returns:
            Document with cleaned text
        """
        # First clean the full text
        document.extracted_text = self._clean_text(document.extracted_text)
        
        # Then clean each page individually
        for page_num, text in document.text_by_page.items():
            document.text_by_page[page_num] = self._clean_text(text)
        
        return document
    
    def _clean_text(self, text: str) -> str:
        """
        Apply cleaning operations to a text string.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return text
            
        # Normalize special characters
        if self.normalize_characters:
            text = self._normalize_characters(text)
            
        # Fix broken line breaks
        if self.fix_line_breaks:
            text = self._fix_line_breaks(text)
            
        # Remove extra whitespace
        if self.remove_extra_whitespace:
            text = self._remove_extra_whitespace(text)
            
        # Remove headers and footers if requested
        if self.remove_headers_footers:
            text = self._remove_headers_footers(text)
            
        return text
    
    @staticmethod
    def _normalize_characters(text: str) -> str:
        """Normalize special characters and encodings."""
        # Replace common problematic characters
        replacements = {
            '\u2018': "'",  # Left single quotation mark
            '\u2019': "'",  # Right single quotation mark
            '\u201c': '"',  # Left double quotation mark
            '\u201d': '"',  # Right double quotation mark
            '\u2013': '-',  # En dash
            '\u2014': '--', # Em dash
            '\u00a0': ' ',  # Non-breaking space
            '\u00ad': '-',  # Soft hyphen
            '\u00b7': '*',  # Middle dot
            '\uf0b7': '*',  # Bullet
            '\u2022': '*',  # Bullet
            '\u2026': '...', # Ellipsis
            '\u00a9': '(c)', # Copyright sign
            '\u00ae': '(R)', # Registered sign
        }
        
        for orig, repl in replacements.items():
            text = text.replace(orig, repl)
            
        return text
    
    @staticmethod
    def _fix_line_breaks(text: str) -> str:
        """Fix incorrect line breaks in paragraphs."""
        # Remove line breaks that occur in the middle of sentences
        text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)  # Remove hyphenation across lines
        text = re.sub(r'(\w)\s*\n\s*(\w)', r'\1 \2', text)  # Join words separated by line breaks
        
        # Preserve paragraph breaks (blank lines)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text
    
    @staticmethod
    def _remove_extra_whitespace(text: str) -> str:
        """Remove redundant whitespace."""
        # Replace multiple spaces with a single space
        text = re.sub(r' +', ' ', text)
        
        # Remove spaces at the beginning of lines
        text = re.sub(r'\n ', '\n', text)
        
        # Remove extra blank lines (more than 2 in a row)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Trim leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _remove_headers_footers(self, text: str) -> str:
        """Attempt to identify and remove headers and footers."""
        # This is a simplified implementation - a more robust approach would
        # analyze repetitive patterns across multiple pages
        
        lines = text.split('\n')
        if len(lines) < 5:
            return text  # Not enough lines to safely identify headers/footers
        
        # Skip potentially the first and last lines if they look like headers/footers
        # This is a very basic heuristic - a real implementation would be more sophisticated
        filtered_lines = []
        skip_first = False
        skip_last = False
        
        # Simple heuristics: headers/footers are often short and may contain
        # page numbers or document identifiers
        if len(lines[0]) < 80 and (re.search(r'\bpage\b|\d+', lines[0].lower()) or 
                                  len(lines[0].strip()) < 30):
            skip_first = True
            
        if len(lines[-1]) < 80 and (re.search(r'\bpage\b|\d+', lines[-1].lower()) or
                                   len(lines[-1].strip()) < 30):
            skip_last = True
        
        # Build filtered text
        for i, line in enumerate(lines):
            if (i == 0 and skip_first) or (i == len(lines) - 1 and skip_last):
                continue
            filtered_lines.append(line)
            
        return '\n'.join(filtered_lines)