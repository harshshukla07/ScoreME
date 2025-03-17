from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime


@dataclass
class Document:
    """Data model representing an extracted document."""
    
    # Basic properties
    path: str
    filename: str
    extracted_text: str = ""
    text_by_page: Dict[int, str] = field(default_factory=dict)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    page_count: int = 0
    extraction_method: str = ""
    
    # Processing state
    processed: bool = False
    processing_timestamp: datetime = field(default_factory=datetime.now)
    
    # Analysis results
    keywords: List[str] = field(default_factory=list)
    entities: Dict[str, List[str]] = field(default_factory=dict)
    summary: str = ""
    
    def __post_init__(self):
        """Set page count from metadata if available."""
        if 'pages' in self.metadata:
            self.page_count = self.metadata['pages']
        elif self.text_by_page:
            self.page_count = max(self.text_by_page.keys()) + 1