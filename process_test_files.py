import os
import sys
from src.extractors.extractor_factory import ExtractorFactory
from src.models.document import Document
from processor_pipeline import ProcessorPipeline
from processor_factory import ProcessorFactory
from src.utils.file_utils import save_document
from src.utils.config import Config


def process_test_files():
    """Process the test PDF files with all available extractors and processors."""
    # Define paths to test files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [
        os.path.join(os.path.dirname(base_dir), "test3.pdf"),
        os.path.join(os.path.dirname(base_dir), "test6.pdf")
    ]
    
    # Create output directory
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Try different extractors
    extractors = ['pypdf', 'pdfplumber', 'ocr']
    
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"File not found: {test_file}")
            continue
            
        print(f"\n\nProcessing: {os.path.basename(test_file)}")
        print("=" * 50)
        
        for extractor_type in extractors:
            try:
                print(f"\nUsing extractor: {extractor_type}")
                print("-" * 30)
                
                # Create extractor
                extractor = ExtractorFactory.create_extractor(extractor_type)
                
                # Extract text
                print("Extracting text...")
                extracted_text = extractor.extract_text(test_file)
                text_by_page = extractor.extract_text_by_page(test_file)
                metadata = extractor.get_metadata(test_file)
                
                # Create document
                doc = Document(
                    path=test_file,
                    filename=os.path.basename(test_file),
                    extracted_text=extracted_text,
                    text_by_page=text_by_page,
                    metadata=metadata,
                    extraction_method=extractor_type
                )
                
                # Process document
                print("Processing text...")
                processors = ProcessorFactory.create_default_processors()
                pipeline = ProcessorPipeline(processors)
                processed_doc = pipeline.process(doc)
                
                # Save results
                file_prefix = f"{os.path.splitext(os.path.basename(test_file))[0]}_{extractor_type}"
                ext_output_dir = os.path.join(output_dir, file_prefix)
                os.makedirs(ext_output_dir, exist_ok=True)
                
                save_options = {
                    'save_text': True,
                    'save_json': True,
                    'save_pages': True
                }
                
                saved_files = save_document(processed_doc, ext_output_dir, save_options)
                
                # Print sample results
                print(f"Pages found: {processed_doc.page_count}")
                
                if processed_doc.keywords:
                    print("\nTop keywords:")
                    for keyword in processed_doc.keywords[:5]:
                        print(f"- {keyword}")
                        
                if processed_doc.entities:
                    print("\nEntities found:")
                    for entity_type, entities in processed_doc.entities.items():
                        if entities:
                            print(f"- {entity_type}: {len(entities)}")
                
                print(f"\nOutput saved to: {ext_output_dir}")
                
                # Print sample of extracted text
                if extracted_text:
                    print("\nSample text:")
                    print("-" * 30)
                    sample = extracted_text[:300]
                    print(sample + "..." if len(extracted_text) > 300 else extracted_text)
                else:
                    print("No text extracted!")
                
            except Exception as e:
                print(f"Error processing with {extractor_type}: {str(e)}")


if __name__ == "__main__":
    process_test_files()