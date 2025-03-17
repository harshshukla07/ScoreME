from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseExtractor(ABC):
    """Abstract base class for all PDF text extractors."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the extractor with optional configuration.
        
        Args:
            config: Dictionary containing configuration parameters
        """
        self.config = config or {}
    
    @abstractmethod
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        pass
    
    @abstractmethod
    def extract_text_by_page(self, pdf_path: str) -> Dict[int, str]:
        """
        Extract text from a PDF file, organized by page.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary mapping page numbers (0-indexed) to extracted text
        """
        pass
    
    def get_metadata(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract metadata from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing metadata fields
        """
        return {}  # Default implementation returns empty metadata