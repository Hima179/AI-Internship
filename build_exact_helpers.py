import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import docx2pdf
import pypdf

WORKSPACE = r"d:\AI INTERNSHIP"
OUTPUT_DOCX = os.path.join(WORKSPACE, "HimanshuPathak_UAI05BT12417_SIP_HANDBOOK.docx")
OUTPUT_PDF = os.path.join(WORKSPACE, "HimanshuPathak_UAI05BT12417_SIP_HANDBOOK.pdf")
DOWNLOADS_DOCX = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_UAI05BT12417_SIP_HANDBOOK.docx"
DOWNLOADS_PDF = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_UAI05BT12417_SIP_HANDBOOK.pdf"

LOGO_HEADER_IMG = os.path.join(WORKSPACE, "extracted_ref_images", "p1_Image23.png")
if not os.path.exists(LOGO_HEADER_IMG):
    LOGO_HEADER_IMG = os.path.join(WORKSPACE, "sandesh_extracted_logo.png")

WEEKLY_LOGO_IMG = os.path.join(WORKSPACE, "akhil_header_logo.png")
STUDENT_SIGNATURE_IMG = os.path.join(WORKSPACE, "himanshu_student_signature.png")
OFFER_LETTER_IMG = os.path.join(WORKSPACE, "himanshu_internship_letter.jpg")

FIG1_1 = os.path.join(WORKSPACE, "report_figures", "fig1_1_methodology_flow.png")
FIG1_2 = os.path.join(WORKSPACE, "report_figures", "fig1_2_er_diagram.png")
FIG1_3 = os.path.join(WORKSPACE, "report_figures", "fig1_3_state_machine.png")
FIG1_4 = os.path.join(WORKSPACE, "report_figures", "fig1_4_testing_pyramid.png")

COLOR_BLACK = RGBColor(0x00, 0x00, 0x00)
COLOR_UNI_BLUE = RGBColor(0x2F, 0x54, 0x96)
COLOR_ACT_GREEN = RGBColor(0x76, 0x9A, 0x49)
COLOR_SCHOOL_GREEN = RGBColor(0x3A, 0x7C, 0x22)

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'</w:tblBorders>')
    tblPr.append(borders)

def format_cell(cell, text, bold=False, font_size=11, font_name="Calibri", align=WD_ALIGN_PARAGRAPH.LEFT, color=COLOR_BLACK, italic=False):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def add_heading_1(doc, text, space_before=14, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK
    return p

def add_heading_2(doc, text, space_before=10, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK
    return p

def add_heading_3(doc, text, space_before=8, space_after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK
    return p

def add_body_p(doc, text="", space_before=0, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.color.rgb = COLOR_BLACK
    return p

def add_bullet_item(doc, bold_prefix, text, space_after=3):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)
        r1.bold = True
        r1.font.color.rgb = COLOR_BLACK
    r2 = p.add_run(text)
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(12)
    r2.font.color.rgb = COLOR_BLACK
    return p

def add_figure(doc, img_path, caption, width_inches=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        r = p_img.add_run()
        r.add_picture(img_path, width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(1)
    p_cap.paragraph_format.space_after = Pt(8)
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(11)
    r_cap.italic = False
    r_cap.font.color.rgb = COLOR_BLACK

def configure_main_section(sec):
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    
    # Start page number at 2
    secPr = sec._sectPr
    pgNumType = parse_xml(r'<w:pgNumType %s w:start="2"/>' % nsdecls('w'))
    secPr.append(pgNumType)

    # Header with university logo at top left
    header = sec.header
    p_head = header.paragraphs[0]
    p_head.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_head.paragraph_format.space_before = Pt(0)
    p_head.paragraph_format.space_after = Pt(0)
    if os.path.exists(LOGO_HEADER_IMG):
        r_head = p_head.add_run()
        r_head.add_picture(LOGO_HEADER_IMG, width=Inches(1.46))

    # Footer with centered Calibri 11pt page number
    footer = sec.footer
    p_foot = footer.paragraphs[0]
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(0)
    p_foot.paragraph_format.space_after = Pt(0)
    r_foot = p_foot.add_run()
    r_foot.font.name = "Calibri"
    r_foot.font.size = Pt(11)
    r_foot.font.color.rgb = COLOR_BLACK
    
    fld1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instr = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fld2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fld3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    r_foot._r.append(fld1)
    r_foot._r.append(instr)
    r_foot._r.append(fld2)
    r_foot._r.append(fld3)

print("Setup helper functions complete.")
