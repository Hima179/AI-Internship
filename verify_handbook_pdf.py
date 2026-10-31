import fitz
import re

pdf_path = "HimanshuPathak_UAI05BT12417_SIP_HANDBOOK.pdf"
doc = fitz.open(pdf_path)
print(f"Total pages in generated PDF: {len(doc)}")

info_found = []
aicell_found = []

for i, page in enumerate(doc):
    text = page.get_text("text")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    first_few = " | ".join(lines[:2]) if lines else "EMPTY"
    last_line = lines[-1] if lines else "EMPTY"
    
    if "info@universalai.in" in text:
        info_found.append(i + 1)
    if "aicell@universalai.in" in text:
        aicell_found.append(i + 1)
        
    print(f"Page {i+1:2d}: First: {first_few[:50]:<50} | Last: {last_line}")

print("\n--- Verification Summary ---")
print(f"Total Page Count: {len(doc)} (Target: 43)")
print(f"info@universalai.in found on pages: {info_found} (Target: None)")
print(f"aicell@universalai.in found on pages: {aicell_found}")
