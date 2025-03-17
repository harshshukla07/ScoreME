import os
import logging
from datetime import datetime


class Logger:
    """Custom logger for the PDF processor."""
    
    def __init__(self, log_dir: str = None, log_level=logging.INFO):
        """
        Initialize the logger.
        
        Args:
            log_dir: Directory for log files (if None, logging to console only)
            log_level: Logging level
        """
        self.logger = logging.getLogger('pdf_processor')
        self.logger.setLevel(log_level)
        self.logger.handlers = []  # Clear any existing handlers
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # Create file handler if log_dir is provided
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"pdf_processor_{timestamp}.log")
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log critical message."""
        self.logger.critical(message)