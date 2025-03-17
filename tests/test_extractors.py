import os
import unittest
import tempfile
from src.extractors.pypdf_extractor import PyPDFExtractor
from src.extractors.pdf_plumber_extractor import PDFPlumberExtractor


class TestExtractors(unittest.TestCase):
    """Test cases for PDF extractors."""
    
    def setUp(self):
        """Set up test environment."""
        # Path to test PDFs - adjust these to point to your test PDFs
        test_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.test_pdf_path = os.path.join(test_dir, "test3.pdf")
        
    def test_pypdf_extractor(self):
        """Test PyPDFExtractor functionality."""
        if not os.path.exists(self.test_pdf_path):
            self.skipTest(f"Test PDF not found: {self.test_pdf_path}")
            
        extractor = PyPDFExtractor()
        
        # Test text extraction
        text = extractor.extract_text(self.test_pdf_path)
        self.assertIsInstance(text, str)
        
        # Test page-by-page extraction
        pages = extractor.extract_text_by_page(self.test_pdf_path)
        self.assertIsInstance(pages, dict)
        
        # Test metadata extraction
        metadata = extractor.get_metadata(self.test_pdf_path)
        self.assertIsInstance(metadata, dict)
        self.assertIn('pages', metadata)
    
    def test_pdfplumber_extractor(self):
        """Test PDFPlumberExtractor functionality."""
        if not os.path.exists(self.test_pdf_path):
            self.skipTest(f"Test PDF not found: {self.test_pdf_path}")
            
        extractor = PDFPlumberExtractor()
        
        # Test text extraction
        text = extractor.extract_text(self.test_pdf_path)
        self.assertIsInstance(text, str)
        
        # Test page-by-page extraction
        pages = extractor.extract_text_by_page(self.test_pdf_path)
        self.assertIsInstance(pages, dict)
        
        # Test metadata extraction
        metadata = extractor.get_metadata(self.test_pdf_path)
        self.assertIsInstance(metadata, dict)
        self.assertIn('pages', metadata)


if __name__ == "__main__":
    unittest.main()