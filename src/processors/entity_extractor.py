import re
from typing import Dict, Any, Optional, List
from ..models.document import Document
from .base_processor import BaseProcessor


class EntityExtractor(BaseProcessor):
    """Extract structured entities from document text."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the entity extractor.
        
        Args:
            config: Configuration dictionary that may include:
                - extract_emails: Extract email addresses (default: True)
                - extract_phones: Extract phone numbers (default: True)
                - extract_urls: Extract URLs (default: True)
                - extract_dates: Extract dates (default: True)
        """
        super().__init__(config)
        self.extract_emails = self.config.get('extract_emails', True)
        self.extract_phones = self.config.get('extract_phones', True)
        self.extract_urls = self.config.get('extract_urls', True)
        self.extract_dates = self.config.get('extract_dates', True)
    
    def process(self, document: Document) -> Document:
        """
        Extract entities from the document.
        
        Args:
            document: Document object with extracted text
            
        Returns:
            Document with extracted entities
        """
        if not document.extracted_text:
            return document
        
        # Initialize entity dictionary
        document.entities = {}
        
        # Extract various entity types based on configuration
        if self.extract_emails:
            document.entities['emails'] = self._extract_emails(document.extracted_text)
            
        if self.extract_phones:
            document.entities['phones'] = self._extract_phones(document.extracted_text)
            
        if self.extract_urls:
            document.entities['urls'] = self._extract_urls(document.extracted_text)
            
        if self.extract_dates:
            document.entities['dates'] = self._extract_dates(document.extracted_text)
            
        return document
    
    @staticmethod
    def _extract_emails(text: str) -> List[str]:
        """Extract email addresses from text."""
        # Email regex pattern
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return sorted(set(re.findall(pattern, text)))
    
    @staticmethod
    def _extract_phones(text: str) -> List[str]:
        """Extract phone numbers from text."""
        # Phone number patterns (handles various formats)
        patterns = [
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 123-456-7890
            r'\b\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}\b',  # (123) 456-7890
            r'\b\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'  # +1 123-456-7890
        ]
        
        phones = []
        for pattern in patterns:
            phones.extend(re.findall(pattern, text))
            
        return sorted(set(phones))
    
    @staticmethod
    def _extract_urls(text: str) -> List[str]:
        """Extract URLs from text."""
        # URL pattern
        pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*'
        return sorted(set(re.findall(pattern, text)))
    
    @staticmethod
    def _extract_dates(text: str) -> List[str]:
        """Extract dates from text."""
        # Date patterns (various formats)
        patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or DD/MM/YYYY
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',  # Month DD, YYYY
            r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b',  # DD Month YYYY
        ]
        
        dates = []
        for pattern in patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
            
        return sorted(set(dates))