#!/usr/bin/env python3
import pdfplumber
import sys

def extract_pdf_text(pdf_path):
    try:
        text_content = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_content += f"\n=== Page {page_num} ===\n"
                    text_content += text + "\n"
        return text_content
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    result = extract_pdf_text(pdf_file)
    print(result)