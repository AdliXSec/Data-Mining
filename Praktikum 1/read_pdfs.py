import fitz
import sys
sys.stdout.reconfigure(encoding='utf-8')

for pdf_name in ['[IND] Modul 1 - Data Preparation (2).pdf', '[IDN] Modul 2 - Pemodelan Data (1).pdf']:
    print(f"\n{'='*80}")
    print(f"FILE: {pdf_name}")
    print(f"{'='*80}")
    doc = fitz.open(pdf_name)
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            print(f"\n--- Page {page_num+1} ---")
            print(text[:3000])
    doc.close()
