# PDF Text Extraction Tool
 A robust, multi-engine tool for extracting and analyzing text from PDF documents. This tool supports various extraction methods to handle different types of PDFs including scanned documents.

## Features 
### Multiple extraction engines:

- **PyPDF2** - Fast extraction for simple PDFs 
- **PDFPlumber** - More accurate extraction with better formatting preservation 
- **OCR** - Extract text from scanned PDFs or images using Tesseract 
### Advanced processing:

- **Text cleaning and normalization** 
- **Content analysis with keyword extraction** 
- **Entity extraction (emails, phone numbers, URLs, dates)** 
- **Page-by-page extraction**

### Flexible output options:

- **Full document text** 
- **Page-by-page text files** 
- **JSON output with metadata**

## Installation 
### Prerequisites 
- **Python 3.7+**
- **For OCR functionality:** 
  - Tesseract OCR (Windows, macOS, Linux) Poppler (Windows, macOS - brew install 
  - poppler, Linux - apt-get install poppler-utils)

### Installation Steps 
1. Clone or download this repository 
   ```sh
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
2. Install Python dependencies: 
   ```sh 
   pip install -r requirements.txt 
3. If using OCR functionality, ensure Tesseract is in your PATH or configure its location in src/extractors/ocr_extractor.py.

## Usage 
### Basic Usage

1. Extract text from a single PDF with default settings: 
   ```sh
   python main.py path/to/your/document.pdf

2. Save extracted text to a specific directory: 
   ```sh 
   python main.py 
   path/to/your/document.pdf --output output_directory

### Choosing an Extraction Method 
1. Specify which extraction engine to use: 
   ```sh
   python main.py path/to/your/document.pdf --extractor [pypdf|pdfplumber|ocr|auto]

- pypdf: Fast extraction, good for text-based PDFs 
- pdfplumber: Better formatting preservation, handles tables well 
- ocr: Best for scanned documents or PDFs with embedded images 
- auto: Automatically selects appropriate extractor (default)

### Processing Test Files Process the sample test files with all available extractors: 

python process_test_files.py

This will process both test3.pdf and test6.pdf using each available extractor and save the results in the output directory.

Batch Processing Process all PDFs in a directory: python main.py path/to/pdf/directory --output output_directory

Output Structure When using the --output option, the following files/directories are created:

{filename}.txt - Complete extracted text from the document {filename}_pages/ - Directory containing page-by-page text files: page_1.txt, page_2.txt, etc. - Text extracted from individual pages When using process_test_files.py, additional analysis results are saved in:

{filename}_{extractor}/ - Directory for each extractor method results Contains full text, page files, and analysis results

Project Structure: text-extraction/ │ ├── main.py # Main entry point ├── process_test_files.py # Script to process test PDFs ├── processor_factory.py # Factory for creating text processors ├── processor_pipeline.py # Pipeline for document processing ├── requirements.txt # Python dependencies ├── output/ # Output directory │ ├── src/ # Source code │ ├── extractors/ # PDF extraction engines │ │ ├── base_extractor.py # Abstract base class │ │ ├── pypdf_extractor.py # PyPDF2 implementation │ │ ├── pdfplumber_extractor.py # PDFPlumber implementation │ │ └── ocr_extractor.py # OCR-based extraction │ │ │ ├── processors/ # Text processing modules │ │ ├── base_processor.py # Abstract base class │ │ ├── text_processor.py # Text cleaning │ │ ├── content_analyzer.py # Content analysis │ │ └── entity_extractor.py # Entity extraction │ │ │ ├── models/ # Data models │ │ └── document.py # Document data model │ │ │ └── utils/ # Utility functions │ └── tests/ # Unit tests

Troubleshooting Missing Dependencies If you get ModuleNotFoundError for any package, install it using pip:

pip install [package_name]

OCR Issues Ensure Tesseract is installed and in your PATH For Windows users, you may need to explicitly set the Tesseract path in src/extractors/ocr_extractor.py: convert_from_path(pdf_path, dpi=300, poppler_path=r'C:\path\to\poppler\bin')
