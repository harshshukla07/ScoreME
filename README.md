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



