from typing import List, Dict, Any, Optional
from src.models.document import Document
from src.processors.base_processor import BaseProcessor
from processor_factory import ProcessorFactory


class ProcessorPipeline:
    """Pipeline for processing documents through multiple processors."""
    
    def __init__(self, processors: Optional[List[BaseProcessor]] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the processor pipeline.
        
        Args:
            processors: List of processor instances
            config: Configuration for creating default processors if none provided
        """
        if processors:
            self.processors = processors
        else:
            self.processors = ProcessorFactory.create_default_processors(config)
    
    def process(self, document: Document) -> Document:
        """
        Process a document through all processors in the pipeline.
        
        Args:
            document: Document to process
            
        Returns:
            Processed document
        """
        for processor in self.processors:
            try:
                document = processor.process(document)
            except Exception as e:
                print(f"Error in processor {processor.__class__.__name__}: {str(e)}")
        
        document.processed = True
        return document
    
    def add_processor(self, processor: BaseProcessor) -> None:
        """
        Add a processor to the pipeline.
        
        Args:
            processor: Processor to add
        """
        self.processors.append(processor)