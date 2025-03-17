import os
import tempfile
from typing import Dict, Any
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from .base_extractor import BaseExtractor


class OCRExtractor(BaseExtractor):
    """PDF text extractor using OCR via Tesseract."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the OCR extractor.
        
        Args:
            config: Configuration dictionary that may include:
                - tesseract_cmd: Path to Tesseract executable
                - lang: OCR language (default: 'eng')
                - dpi: DPI for PDF rendering (default: 300)
        """
        super().__init__(config)
        
        # Set Tesseract command if provided
        if self.config.get('tesseract_cmd'):
            pytesseract.pytesseract.tesseract_cmd = self.config.get('tesseract_cmd')
            
        # Default configuration
        self.lang = self.config.get('lang', 'eng')
        self.dpi = self.config.get('dpi', 300)
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file using OCR.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        full_text = ""
        
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=self.dpi)
            
            # Process each image with OCR
            for image in images:
                text = pytesseract.image_to_string(image, lang=self.lang)
                if text:
                    full_text += text + "\n\n"
        except Exception as e:
            print(f"Error extracting text with OCR: {str(e)}")
            return ""
            
        return full_text.strip()
    
    def extract_text_by_page(self, pdf_path: str) -> Dict[int, str]:
        """
        Extract text from a PDF file using OCR, organized by page.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary mapping page numbers (0-indexed) to extracted text
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        pages_text = {}
        
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=self.dpi)
            
            # Process each image with OCR
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image, lang=self.lang)
                if text:
                    pages_text[i] = text
                else:
                    pages_text[i] = ""
        except Exception as e:
            print(f"Error extracting text with OCR: {str(e)}")
            return {}
            
        return pages_text
    
    def get_metadata(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract basic metadata from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing basic metadata
        """
        metadata = {}
        
        try:
            # Convert PDF to images to count pages
            images = convert_from_path(pdf_path, dpi=self.dpi)
            metadata = {
                'pages': len(images),
                'extraction_method': 'ocr',
                'ocr_lang': self.lang,
                'dpi': self.dpi
            }
        except Exception as e:
            print(f"Error extracting metadata with OCR: {str(e)}")
            
        return metadata