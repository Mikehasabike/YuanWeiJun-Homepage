#!/usr/bin/env python3
import sys
import os

try:
    # 尝试导入pdfplumber
    import pdfplumber
    print("pdfplumber已安装")
    
    pdf_path = "cv_weijun-yuan_short.pdf"
    if os.path.exists(pdf_path):
        print(f"找到PDF文件: {pdf_path}")
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            print("=== PDF内容提取 ===")
            print(text[:2000])  # 打印前2000个字符
            print("=== 结束 ===")
            
            # 保存到文件
            with open("cv_extracted.txt", "w", encoding="utf-8") as f:
                f.write(text)
            print("内容已保存到 cv_extracted.txt")
    else:
        print(f"PDF文件不存在: {pdf_path}")
        
except ImportError:
    print("pdfplumber未安装，尝试安装...")
    # 这里只是显示消息，实际安装需要用户交互
    print("请手动安装pdfplumber: pip install pdfplumber")
    
except Exception as e:
    print(f"错误: {e}")