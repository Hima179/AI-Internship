import pymupdf

doc = pymupdf.open(r"d:\AI INTERNSHIP\Akhil_Barman_UAI05BT12405_SIP_HANDBOOK_removed.pdf")

for pno in range(30, 43):
    page = doc[pno]
    print(f"\n======================================== PAGE {pno+1} ========================================")
    td = page.get_text("dict")
    for b in td["blocks"]:
        if "lines" in b:
            for l in b["lines"]:
                spans_out = []
                for s in l["spans"]:
                    t = s["text"].strip()
                    if t:
                        c = f"#{s['color']:06x}"
                        spans_out.append(f"{t} [{s['font']}, {s['size']:.1f}pt, {c}]")
                if spans_out:
                    print(" | ".join(spans_out))
        elif "image" in b:
            print(f"[IMAGE bbox={b['bbox']}]")
