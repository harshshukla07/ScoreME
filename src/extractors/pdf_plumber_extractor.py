import os
from typing import Dict, Any
import pdfplumber
from .base_extractor import BaseExtractor


class PDFPlumberExtractor(BaseExtractor):
    """PDF text extractor using PDFPlumber library."""
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file using PDFPlumber.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        full_text = ""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n\n"
        except Exception as e:
            print(f"Error extracting text with PDFPlumber: {str(e)}")
            return ""
            
        return full_text.strip()
    
    def extract_text_by_page(self, pdf_path: str) -> Dict[int, str]:
        """
        Extract text from a PDF file, organized by page.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary mapping page numbers (0-indexed) to extracted text
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        pages_text = {}
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        pages_text[i] = text
                    else:
                        pages_text[i] = ""
        except Exception as e:
            print(f"Error extracting text with PDFPlumber: {str(e)}")
            return {}
            
        return pages_text
    
    def get_metadata(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract metadata from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing metadata fields
        """
        metadata = {}
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                metadata = {
                    'pages': len(pdf.pages),
                }
                
                # Try to extract document info if available
                if hasattr(pdf, 'metadata') and pdf.metadata:
                    for key, value in pdf.metadata.items():
                        metadata[key] = value
                            
        except Exception as e:
            print(f"Error extracting metadata with PDFPlumber: {str(e)}")
            
        return metadata