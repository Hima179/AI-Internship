import pptx

prs = pptx.Presentation(r"C:\Users\Himanshu Pathak\Downloads\FlowCore_Digital_SIP_Presentation.pptx")
for i in range(4):
    slide = prs.slides[i]
    print(f"=== SLIDE {i+1} ===")
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                txt = p.text.strip()
                if txt:
                    font_info = []
                    for r in p.runs:
                        fn = r.font.name
                        fs = r.font.size.pt if r.font.size else "inherit"
                        bold = r.font.bold
                        try:
                            c = str(r.font.color.rgb) if r.font.color and r.font.color.type == pptx.enum.dml.MSO_COLOR_TYPE.RGB else "theme"
                        except:
                            c = "theme"
                        font_info.append(f"{fn}/{fs}pt/b={bold}/c={c}")
                    print(f"  [{shape.name}]: \"{txt[:50]}\" -> {font_info[:1]}")
