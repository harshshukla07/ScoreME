import re
from collections import Counter
from typing import Dict, Any, Optional, List
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from ..models.document import Document
from .base_processor import BaseProcessor


class ContentAnalyzer(BaseProcessor):
    """Analyze document content and extract key information."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the content analyzer.
        
        Args:
            config: Configuration dictionary that may include:
                - extract_keywords: Extract keywords (default: True)
                - num_keywords: Number of keywords to extract (default: 15)
                - language: Text language for analysis (default: 'english')
                - generate_summary: Generate text summary (default: False)
        """
        super().__init__(config)
        self.extract_keywords = self.config.get('extract_keywords', True)
        self.num_keywords = self.config.get('num_keywords', 15)
        self.language = self.config.get('language', 'english')
        self.generate_summary = self.config.get('generate_summary', False)
        
        # Download necessary NLTK resources if needed
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        try:
            nltk.data.find(f'corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
    
    def process(self, document: Document) -> Document:
        """
        Analyze the document content.
        
        Args:
            document: Document object with extracted text
            
        Returns:
            Document with analysis results
        """
        if not document.extracted_text:
            return document
            
        # Extract keywords
        if self.extract_keywords:
            document.keywords = self._extract_keywords(document.extracted_text)
            
        # Generate summary if requested
        if self.generate_summary:
            document.summary = self._generate_summary(document.extracted_text)
            
        return document
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract the most important keywords from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of keywords
        """
        try:
            # Tokenize and prepare words
            words = word_tokenize(text.lower())
            
            # Remove stopwords, numbers, and short words
            stop_words = set(stopwords.words(self.language))
            words = [word for word in words if word.isalpha() and word not in stop_words and len(word) > 2]
            
            # Get most common words
            word_freq = Counter(words)
            keywords = [word for word, _ in word_freq.most_common(self.num_keywords)]
            
            return keywords
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return []
    
    def _generate_summary(self, text: str) -> str:
        """
        Generate a summary of the text using extractive summarization.
        
        Args:
            text: Text to summarize
            
        Returns:
            Summary text
        """
        try:
            # Split into sentences
            sentences = sent_tokenize(text)
            
            if len(sentences) <= 5:
                return text  # Text is already short, return as is
                
            # Simple extractive summarization: use first few sentences
            # A more sophisticated approach would use sentence ranking
            summary = ' '.join(sentences[:5])
            
            return summary
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return text[:500] + "..."  # Fallback to simple truncation