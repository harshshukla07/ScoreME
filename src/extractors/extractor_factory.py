from typing import Dict, Any, Optional
from src.extractors.base_extractor import BaseExtractor
from src.extractors.pypdf_extractor import PyPDFExtractor
from src.extractors.pdf_plumber_extractor import PDFPlumberExtractor
from src.extractors.ocr_extractor import OCRExtractor


class ExtractorFactory:
    """Factory class to create appropriate PDF extractors."""
    
    @staticmethod
    def create_extractor(extractor_type: str, config: Optional[Dict[str, Any]] = None) -> BaseExtractor:
        """
        Create an extractor instance based on the specified type.
        
        Args:
            extractor_type: Type of extractor to create ('pypdf', 'pdfplumber', 'ocr', 'auto')
            config: Optional configuration parameters
            
        Returns:
            An instance of the requested extractor
            
        Raises:
            ValueError: If the extractor type is not supported
        """
        config = config or {}
        
        if extractor_type == 'pypdf':
            return PyPDFExtractor(config)
        elif extractor_type == 'pdfplumber':
            return PDFPlumberExtractor(config)
        elif extractor_type == 'ocr':
            return OCRExtractor(config)
        elif extractor_type == 'auto':
            # Auto selection based on PDF content
            return PyPDFExtractor(config)  # Default for now
        else:
            raise ValueError(f"Unsupported extractor type: {extractor_type}")
    
    @staticmethod
    def get_available_extractors() -> list:
        """
        Get a list of available extractor types.
        
        Returns:
            List of available extractor type names
        """
        return ['pypdf', 'pdfplumber', 'ocr', 'auto']