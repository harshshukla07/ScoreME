import os
import sys
import argparse
from src.extractors.extractor_factory import ExtractorFactory
from src.models.document import Document


def process_pdf(pdf_path: str, extractor_type: str = 'auto', output_dir: str = None):
    """
    Process a PDF file: extract text and save results.
    
    Args:
        pdf_path: Path to the PDF file
        extractor_type: Type of extractor to use
        output_dir: Directory to save output files
        
    Returns:
        Document object with extracted contents
    """
    print(f"Processing PDF: {pdf_path}")
    
    # Create extractor
    extractor = ExtractorFactory.create_extractor(extractor_type)
    
    # Extract text and metadata
    extracted_text = extractor.extract_text(pdf_path)
    text_by_page = extractor.extract_text_by_page(pdf_path)
    metadata = extractor.get_metadata(pdf_path)
    
    # Create document object
    filename = os.path.basename(pdf_path)
    doc = Document(
        path=pdf_path,
        filename=filename,
        extracted_text=extracted_text,
        text_by_page=text_by_page,
        metadata=metadata,
        extraction_method=extractor_type
    )
    
    # Save extracted text if output directory is specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
        # Save full text
        text_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        
        # Save page-by-page text
        pages_dir = os.path.join(output_dir, os.path.splitext(filename)[0] + "_pages")
        os.makedirs(pages_dir, exist_ok=True)
        
        for page_num, text in text_by_page.items():
            page_path = os.path.join(pages_dir, f"page_{page_num + 1}.txt")
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(text)
    
    return doc


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Extract text from PDF files")
    parser.add_argument("pdf_path", help="Path to PDF file or directory of PDF files")
    parser.add_argument("--extractor", choices=ExtractorFactory.get_available_extractors(),
                        default='auto', help="Extraction method to use")
    parser.add_argument("--output", help="Output directory for extracted text")
    
    args = parser.parse_args()
    
    # Process single file or directory
    if os.path.isdir(args.pdf_path):
        # Process all PDFs in directory
        pdf_files = [os.path.join(args.pdf_path, f) for f in os.listdir(args.pdf_path)
                    if f.lower().endswith('.pdf')]
        
        for pdf_file in pdf_files:
            try:
                doc = process_pdf(pdf_file, args.extractor, args.output)
                print(f"Successfully processed: {doc.filename}, {doc.page_count} pages")
            except Exception as e:
                print(f"Error processing {pdf_file}: {str(e)}")
    else:
        # Process single PDF file
        if not os.path.isfile(args.pdf_path):
            print(f"Error: File not found: {args.pdf_path}")
            sys.exit(1)
        
        try:
            doc = process_pdf(args.pdf_path, args.extractor, args.output)
            print(f"Successfully processed: {doc.filename}, {doc.page_count} pages")
            
            # Print sample of extracted text
            if doc.extracted_text:
                print("\nSample extracted text:")
                print("-" * 50)
                # Show first 300 characters of the extracted text
                sample = doc.extracted_text[:300]
                print(sample + "..." if len(doc.extracted_text) > 300 else doc.extracted_text)
                print("-" * 50)
            else:
                print("Warning: No text was extracted from the PDF.")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()