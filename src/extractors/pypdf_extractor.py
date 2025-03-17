import os
from typing import Dict, Any
import PyPDF2
from .base_extractor import BaseExtractor


class PyPDFExtractor(BaseExtractor):
    """PDF text extractor using PyPDF2 library."""
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file using PyPDF2.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        full_text = ""
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n\n"
        except Exception as e:
            print(f"Error extracting text with PyPDF2: {str(e)}")
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
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        pages_text[page_num] = text
                    else:
                        pages_text[page_num] = ""
        except Exception as e:
            print(f"Error extracting text with PyPDF2: {str(e)}")
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
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                metadata = {
                    'pages': len(reader.pages),
                }
                
                if reader.metadata:
                    for key, value in reader.metadata.items():
                        if key.startswith('/'):
                            clean_key = key[1:]  # Remove leading slash
                            metadata[clean_key] = value
                        else:
                            metadata[key] = value
                            
        except Exception as e:
            print(f"Error extracting metadata with PyPDF2: {str(e)}")
            
        return metadata