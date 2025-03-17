import unittest
from src.models.document import Document
from src.processors.text_processor import TextProcessor
from src.processors.content_analyzer import ContentAnalyzer
from src.processors.entity_extractor import EntityExtractor


class TestProcessors(unittest.TestCase):
    """Test cases for text processors."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a sample document
        self.sample_text = """
        This is a test document created on January 15, 2023.
        It contains some sample text for testing the processors.
        Contact us at example@example.com or call +1 (555) 123-4567.
        Visit our website at https://www.example.com for more information.
        """
        
        self.document = Document(
            path="/path/to/test.pdf",
            filename="test.pdf",
            extracted_text=self.sample_text,
            text_by_page={0: self.sample_text}
        )
    
    def test_text_processor(self):
        """Test TextProcessor functionality."""
        processor = TextProcessor()
        processed_doc = processor.process(self.document)
        
        self.assertIsInstance(processed_doc, Document)
        self.assertIsNotNone(processed_doc.extracted_text)
    
    def test_content_analyzer(self):
        """Test ContentAnalyzer functionality."""
        processor = ContentAnalyzer()
        processed_doc = processor.process(self.document)
        
        self.assertIsInstance(processed_doc, Document)
        self.assertIsInstance(processed_doc.keywords, list)
    
    def test_entity_extractor(self):
        """Test EntityExtractor functionality."""
        processor = EntityExtractor()
        processed_doc = processor.process(self.document)
        
        self.assertIsInstance(processed_doc, Document)
        self.assertIsInstance(processed_doc.entities, dict)
        
        # Check for specific entities
        self.assertIn('emails', processed_doc.entities)
        self.assertIn('urls', processed_doc.entities)
        self.assertIn('example@example.com', processed_doc.entities['emails'])
        self.assertIn('https://www.example.com', processed_doc.entities['urls'])


if __name__ == "__main__":
    unittest.main()