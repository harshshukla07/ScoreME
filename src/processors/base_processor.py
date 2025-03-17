from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..models.document import Document


class BaseProcessor(ABC):
    """Base class for text processors."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the text processor.
        
        Args:
            config: Configuration dictionary for the processor
        """
        self.config = config or {}
    
    @abstractmethod
    def process(self, document: Document) -> Document:
        """
        Process the document and return the updated document.
        
        Args:
            document: Document object to process
            
        Returns:
            Processed document
        """
        pass