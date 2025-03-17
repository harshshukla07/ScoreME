import os
import json
import shutil
from typing import Dict, List, Any
from ..models.document import Document


def ensure_dir(directory: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Directory path to create
    """
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def find_pdf_files(path: str) -> List[str]:
    """
    Find all PDF files in a directory or return a single PDF path.
    
    Args:
        path: Path to a PDF file or directory containing PDFs
        
    Returns:
        List of PDF file paths
    """
    pdf_files = []
    
    if os.path.isfile(path) and path.lower().endswith('.pdf'):
        pdf_files.append(path)
    elif os.path.isdir(path):
        for file in os.listdir(path):
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(path, file))
                
    return pdf_files


def save_document(document: Document, output_dir: str, save_options: Dict[str, bool] = None) -> Dict[str, str]:
    """
    Save document contents to output directory.
    
    Args:
        document: Document to save
        output_dir: Output directory
        save_options: Options for what to save {'save_text': True, 'save_json': True, 'save_pages': False}
        
    Returns:
        Dictionary of saved file paths
    """
    if save_options is None:
        save_options = {'save_text': True, 'save_json': True, 'save_pages': False}
        
    saved_files = {}
    ensure_dir(output_dir)
    
    basename = os.path.splitext(document.filename)[0]
    
    # Save extracted text
    if save_options.get('save_text', True) and document.extracted_text:
        text_path = os.path.join(output_dir, f"{basename}.txt")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(document.extracted_text)
        saved_files['text'] = text_path
    
    # Save as JSON
    if save_options.get('save_json', True):
        json_path = os.path.join(output_dir, f"{basename}.json")
        
        # Create a simplified version of the document for JSON
        doc_dict = {
            'filename': document.filename,
            'path': document.path,
            'page_count': document.page_count,
            'extraction_method': document.extraction_method,
            'metadata': document.metadata,
            'keywords': document.keywords,
            'entities': document.entities,
            'summary': document.summary,
            'processing_timestamp': document.processing_timestamp.isoformat()
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(doc_dict, f, indent=2)
        saved_files['json'] = json_path
    
    # Save individual pages
    if save_options.get('save_pages', False) and document.text_by_page:
        pages_dir = os.path.join(output_dir, f"{basename}_pages")
        ensure_dir(pages_dir)
        
        for page_num, text in document.text_by_page.items():
            page_path = os.path.join(pages_dir, f"page_{page_num + 1}.txt")
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(text)
        saved_files['pages_dir'] = pages_dir
    
    return saved_files