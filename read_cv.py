import pdfplumber
import sys

def extract_pdf_text(pdf_path):
    text_content = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                text_content += "\n=== Page " + str(page_num) + " ===\n"
                text_content += text + "\n"
    return text_content

pdf_file = "cv_weijun-yuan_short.pdf"
result = extract_pdf_text(pdf_file)
print(result)

with open("cv_extracted.txt", "w", encoding="utf-8") as f:
    f.write(result)
print("\n内容已保存到 cv_extracted.txt")