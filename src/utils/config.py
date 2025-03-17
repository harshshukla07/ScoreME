import os
import json
from typing import Dict, Any


class Config:
    """Configuration management for the PDF processor."""
    
    DEFAULT_CONFIG = {
        'extractors': {
            'default': 'auto',
            'pypdf': {},
            'pdfplumber': {},
            'ocr': {
                'dpi': 300,
                'lang': 'eng'
            }
        },
        'processors': {
            'text_processor': {
                'remove_extra_whitespace': True,
                'fix_line_breaks': True,
                'remove_headers_footers': False,
                'normalize_characters': True
            },
            'content_analyzer': {
                'extract_keywords': True,
                'num_keywords': 15,
                'language': 'english',
                'generate_summary': False
            },
            'entity_extractor': {
                'extract_emails': True,
                'extract_phones': True,
                'extract_urls': True,
                'extract_dates': True
            }
        },
        'output': {
            'save_text': True,
            'save_json': True,
            'save_pages': False
        }
    }
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration from file or defaults.
        
        Args:
            config_path: Path to JSON config file
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and os.path.exists(config_path):
            self.load_from_file(config_path)
    
    def load_from_file(self, config_path: str) -> None:
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to JSON config file
        """
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                self._update_config(self.config, user_config)
        except Exception as e:
            print(f"Error loading config file: {str(e)}")
    
    def _update_config(self, config: Dict[str, Any], updates: Dict[str, Any]) -> None:
        """
        Update configuration recursively.
        
        Args:
            config: Current configuration dictionary
            updates: New values to apply
        """
        for key, value in updates.items():
            if key in config and isinstance(value, dict) and isinstance(config[key], dict):
                self._update_config(config[key], value)
            else:
                config[key] = value
    
    def get(self, section: str = None, key: str = None) -> Any:
        """
        Get configuration value(s).
        
        Args:
            section: Configuration section
            key: Configuration key within section
            
        Returns:
            Configuration value or section
        """
        if section is None:
            return self.config
        
        if section not in self.config:
            return None
        
        if key is None:
            return self.config[section]
        
        return self.config[section].get(key)
    
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key within section
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
    
    def save(self, config_path: str) -> None:
        """
        Save configuration to file.
        
        Args:
            config_path: Path to save JSON config
        """
        try:
            os.makedirs(os.path.dirname(os.path.abspath(config_path)), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config file: {str(e)}")