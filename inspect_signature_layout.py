import pymupdf

doc = pymupdf.open(r"D:\AI INTERNSHIP\SandeshHalmadge_SIP_WeeklyReport.pdf")
page = doc[1] # Page 2
for block in page.get_text("blocks"):
    if any(k in block[4] for k in ["Sandesh", "Signature", "X"]):
        print("Block bbox:", block[:4])
        print("Content:\n", repr(block[4]))

# Also check for drawings (lines) on page 2
drawings = page.get_drawings()
print(f"Total vector drawings on page 2: {len(drawings)}")
for d in drawings:
    # check lines near signature
    rect = d["rect"]
    if rect.y0 > 600:
        print("Drawing near signature:", d["type"], rect)
