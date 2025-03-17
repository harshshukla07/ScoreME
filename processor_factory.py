from typing import Dict, Any, Optional, List
from src.processors.base_processor import BaseProcessor
from src.processors.text_processor import TextProcessor
from src.processors.content_analyzer import ContentAnalyzer
from src.processors.entity_extractor import EntityExtractor


class ProcessorFactory:
    """Factory class to create text processors."""
    
    @staticmethod
    def create_processor(processor_type: str, config: Optional[Dict[str, Any]] = None) -> BaseProcessor:
        """
        Create a processor instance based on the specified type.
        
        Args:
            processor_type: Type of processor to create ('text', 'content', 'entity')
            config: Optional configuration parameters
            
        Returns:
            An instance of the requested processor
            
        Raises:
            ValueError: If the processor type is not supported
        """
        config = config or {}
        
        if processor_type == 'text':
            return TextProcessor(config)
        elif processor_type == 'content':
            return ContentAnalyzer(config)
        elif processor_type == 'entity':
            return EntityExtractor(config)
        else:
            raise ValueError(f"Unsupported processor type: {processor_type}")
    
    @staticmethod
    def create_default_processors(config: Optional[Dict[str, Any]] = None) -> List[BaseProcessor]:
        """
        Create the default processing pipeline.
        
        Args:
            config: Configuration for processors
            
        Returns:
            List of processor instances in recommended order
        """
        text_config = config.get('text_processor', {}) if config else {}
        content_config = config.get('content_analyzer', {}) if config else {}
        entity_config = config.get('entity_extractor', {}) if config else {}
        
        return [
            TextProcessor(text_config),        # First clean the text
            ContentAnalyzer(content_config),   # Then analyze content
            EntityExtractor(entity_config)     # Finally extract entities
        ]
    
    @staticmethod
    def get_available_processors() -> list:
        """
        Get a list of available processor types.
        
        Returns:
            List of available processor type names
        """
        return ['text', 'content', 'entity']