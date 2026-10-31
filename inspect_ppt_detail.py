import pptx
import os

flow_path = r"C:\Users\Himanshu Pathak\Downloads\FlowCore_Digital_SIP_Presentation.pptx"
master_path = r"C:\Users\Himanshu Pathak\Downloads\Master Template for SIP.pptx"

def inspect(path, name):
    print(f"==================================================")
    print(f"=== {name} ===")
    print(f"==================================================")
    prs = pptx.Presentation(path)
    print(f"Slide width: {prs.slide_width/914400:.2f} in, height: {prs.slide_height/914400:.2f} in")
    print(f"Slides count: {len(prs.slides)}")
    
    for i, slide in enumerate(prs.slides):
        print(f"\n--- Slide {i+1} ---")
        for s_idx, shape in enumerate(slide.shapes):
            l, t, w, h = shape.left/914400, shape.top/914400, shape.width/914400, shape.height/914400
            txt = shape.text_frame.text.replace("\n", " \\n ") if shape.has_text_frame else "[NO TEXT]"
            txt_preview = txt[:100] + ("..." if len(txt) > 100 else "")
            shape_type_str = str(shape.shape_type)
            is_pic = "PICTURE" in shape_type_str or shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE
            print(f"  Shape {s_idx} ({shape.name}, type={shape_type_str}, pic={is_pic}): pos=({l:.2f}, {t:.2f}), size=({w:.2f}x{h:.2f}) | {txt_preview}")

if __name__ == "__main__":
    inspect(flow_path, "FLOWCORE DIGITAL (FRIEND'S PPT)")
