from pypdf import PdfReader

pdf_file = "cv_weijun-yuan_short.pdf"

try:
    reader = PdfReader(pdf_file)
    print("PDF pages:", len(reader.pages))
    
    text = ""
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += "=== Page " + str(i+1) + " ===\n"
            text += page_text + "\n"
    
    print(text)
    
    with open("cv_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("\nSaved to cv_text.txt")
    
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()