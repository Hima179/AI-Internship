import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def add_signature_block(doc, student_name="Himanshu Pathak"):
    """Adds a Microsoft Word-style signature line block."""
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(8)
    p_space.paragraph_format.space_after = Pt(2)
    
    tbl = doc.add_table(rows=2, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl.autofit = False
    
    # Cell 0: The "X" signature mark
    cell0 = tbl.rows[0].cells[0]
    cell0.width = Inches(2.6)
    p0 = cell0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(2)
    r_x = p0.add_run("X  ")
    r_x.font.name = "Arial"
    r_x.font.size = Pt(20)
    r_x.font.color.rgb = RGBColor(0, 0, 0)
    
    # Stylized digital signature simulation
    r_sig = p0.add_run("Himanshu Pathak")
    r_sig.font.name = "Brush Script MT"
    r_sig.font.size = Pt(16)
    r_sig.font.italic = True
    r_sig.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
    
    # Cell 1: Signer name under line
    cell1 = tbl.rows[1].cells[0]
    cell1.width = Inches(2.6)
    
    # Add top border to cell1 to act as signature line
    tcPr = cell1._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p1 = cell1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(0)
    r_name = p1.add_run(student_name)
    r_name.font.name = "Segoe UI"
    r_name.font.size = Pt(8.5)
    r_name.font.color.rgb = RGBColor(0, 0, 0)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(10)
    r_lbl = p_sub.add_run("Student Signature: (Digital Signature)")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(11)
    r_lbl.bold = True
    r_lbl.font.color.rgb = RGBColor(0, 0, 0)

print("Signature helper defined.")
