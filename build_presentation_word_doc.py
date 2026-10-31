import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

WORKSPACE = r"d:\AI INTERNSHIP"
OUT_DOCX_WS = os.path.join(WORKSPACE, "HimanshuPathak_UAI05BT12417_SIP_Presentation_Document.docx")
OUT_DOCX_DL = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_UAI05BT12417_SIP_Presentation_Document.docx"
OUT_PDF_WS = os.path.join(WORKSPACE, "HimanshuPathak_UAI05BT12417_SIP_Presentation_Document.pdf")
OUT_PDF_DL = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_UAI05BT12417_SIP_Presentation_Document.pdf"

LOGO_IMG = os.path.join(WORKSPACE, "sandesh_extracted_logo.png")
FIG1_1 = os.path.join(WORKSPACE, "report_figures", "fig1_1_methodology_flow.png")
FIG1_2 = os.path.join(WORKSPACE, "report_figures", "fig1_2_er_diagram.png")
FIG1_3 = os.path.join(WORKSPACE, "report_figures", "fig1_3_state_machine.png")
FIG_BENCHMARK = os.path.join(WORKSPACE, "report_figures", "fig_results_benchmark.png")

# Palette
COLOR_NAVY = RGBColor(0x0F, 0x2D, 0x59)
COLOR_BLUE = RGBColor(0x1E, 0x3A, 0x8A)
COLOR_TEXT = RGBColor(0x1E, 0x29, 0x3B)
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)
COLOR_GREEN = RGBColor(0x16, 0xA3, 0x4A)
COLOR_RED = RGBColor(0xDC, 0x26, 0x26)

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4"):
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

def format_cell(cell, text, bold=False, font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, color=COLOR_TEXT, italic=False):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def add_heading_1(doc, text, space_before=16, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = COLOR_NAVY
    return p

def add_heading_2(doc, text, space_before=12, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = COLOR_BLUE
    return p

def add_heading_3(doc, text, space_before=8, space_after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True
    r.font.color.rgb = COLOR_TEXT
    return p

def add_body_p(doc, text="", space_before=0, space_after=5, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.color.rgb = COLOR_TEXT
    return p

def add_bullet_item(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.0)
        r1.bold = True
        r1.font.color.rgb = COLOR_NAVY
    r2 = p.add_run(text)
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(10.0)
    r2.font.color.rgb = COLOR_TEXT
    return p

def add_speaker_script_box(doc, script_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_cell_background(tbl.rows[0].cells[0], "F8FAFC")
    set_cell_margins(tbl.rows[0].cells[0], top=100, bottom=100, left=160, right=140)
    
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                        f'<w:top w:val="none"/>'
                        f'<w:bottom w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'<w:insideH w:val="none"/>'
                        f'<w:insideV w:val="none"/>'
                        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1E3A8A"/>'
                        f'</w:tblBorders>')
    tbl.rows[0].cells[0]._tc.get_or_add_tcPr().append(borders)
    
    p = tbl.rows[0].cells[0].paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r_head = p.add_run("🎤 Oral Presentation & Speaker Defense Script:\n")
    r_head.font.name = "Times New Roman"
    r_head.font.size = Pt(10.0)
    r_head.bold = True
    r_head.font.color.rgb = COLOR_BLUE
    
    r_body = p.add_run(f'"{script_text}"')
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(9.5)
    r_body.italic = True
    r_body.font.color.rgb = COLOR_TEXT

def add_viva_qa_box(doc, qa_list):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_cell_background(tbl.rows[0].cells[0], "FFFBEB")
    set_cell_margins(tbl.rows[0].cells[0], top=100, bottom=100, left=160, right=140)
    
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                        f'<w:top w:val="none"/>'
                        f'<w:bottom w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'<w:insideH w:val="none"/>'
                        f'<w:insideV w:val="none"/>'
                        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="D97706"/>'
                        f'</w:tblBorders>')
    tbl.rows[0].cells[0]._tc.get_or_add_tcPr().append(borders)
    
    p = tbl.rows[0].cells[0].paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r_head = p.add_run("❓ Key Viva / Defense Questions & Evaluator Answers:\n")
    r_head.font.name = "Times New Roman"
    r_head.font.size = Pt(10.0)
    r_head.bold = True
    r_head.font.color.rgb = RGBColor(0xB4, 0x53, 0x09)
    
    for q, a in qa_list:
        p2 = tbl.rows[0].cells[0].add_paragraph()
        p2.paragraph_format.space_before = Pt(3)
        p2.paragraph_format.space_after = Pt(2)
        
        rq = p2.add_run(f"Q: {q}\n")
        rq.font.name = "Times New Roman"
        rq.font.size = Pt(9.5)
        rq.bold = True
        rq.font.color.rgb = COLOR_NAVY
        
        ra = p2.add_run(f"A: {a}")
        ra.font.name = "Times New Roman"
        ra.font.size = Pt(9.0)
        ra.font.color.rgb = COLOR_TEXT

def add_figure(doc, img_path, caption_text, width_inches=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inches))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = "Times New Roman"
        run_cap.font.size = Pt(9.0)
        run_cap.italic = True
        run_cap.font.color.rgb = COLOR_MUTED

# ===========================================================================
# DOCUMENT BUILDER
# ===========================================================================
def build_document():
    doc = Document()
    
    # Page setup (Letter, 0.8 in margins)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
    # -------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------
    if os.path.exists(LOGO_IMG):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(6)
        r_logo = p_logo.add_run()
        r_logo.add_picture(LOGO_IMG, width=Inches(3.2))

    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(4)
    p_uni.paragraph_format.space_after = Pt(2)
    r = p_uni.add_run("UNIVERSAL AI UNIVERSITY, KARJAT")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.bold = True
    r.font.color.rgb = COLOR_NAVY

    p_sch = doc.add_paragraph()
    p_sch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sch.paragraph_format.space_before = Pt(0)
    p_sch.paragraph_format.space_after = Pt(2)
    r2 = p_sch.add_run("School of AI & Future Technologies")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(13)
    r2.bold = True
    r2.font.color.rgb = COLOR_BLUE

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(16)
    r3 = p_sub.add_run("Established vide Maharashtra Act No. III of 2023 | Recognized by UGC Act 1956")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(9.5)
    r3.italic = True
    r3.font.color.rgb = COLOR_MUTED

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(12)
    p_rep.paragraph_format.space_after = Pt(6)
    r_rep = p_rep.add_run("SUMMER INTERNSHIP PROGRAM (SIP) PRESENTATION DOSSIER")
    r_rep.font.name = "Times New Roman"
    r_rep.font.size = Pt(15)
    r_rep.bold = True
    r_rep.font.color.rgb = COLOR_NAVY

    p_on = doc.add_paragraph()
    p_on.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_on.paragraph_format.space_before = Pt(0)
    p_on.paragraph_format.space_after = Pt(8)
    r_on = p_on.add_run("Complete Slide Deck Transcripts, Architecture Blueprints, and Oral Defense Guide on")
    r_on.font.name = "Times New Roman"
    r_on.font.size = Pt(10.5)
    r_on.italic = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(14)
    r_title = p_title.add_run("Full-Stack AI & Clinical Assessment Systems:\nEngineering the UAi PsychePortal Integrated Suite and\nProductivAI Analytics Engine")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(14)
    r_title.bold = True
    r_title.font.color.rgb = COLOR_BLUE

    # Details table
    tbl = doc.add_table(rows=5, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="E2E8F0", sz="4")
    col_w = [Inches(3.3), Inches(3.3)]
    for row in tbl.rows:
        for idx, w in enumerate(col_w):
            row.cells[idx].width = w

    rows_data = [
        ("Submitted By:", "Under the Guidance of:"),
        ("Himanshu Pathak", "Prof. Rajesh Bhise (Internal Faculty Guide)"),
        ("Roll No.: UAI05BT12417", "Dr. Shivaji Pawar (Head of Department)"),
        ("Batch: 2024 - 2028 (Semester 4)", "School of AI & Future Technologies"),
        ("Internship Tenure: 4-May-2026 to 13-Jun-2026", "AI Cell, Universal AI University, Karjat")
    ]
    for r_idx, (c0, c1) in enumerate(rows_data):
        format_cell(tbl.rows[r_idx].cells[0], c0, bold=(r_idx in [0, 1]), font_size=10, color=COLOR_NAVY if r_idx==1 else COLOR_TEXT)
        format_cell(tbl.rows[r_idx].cells[1], c1, bold=(r_idx == 0), font_size=10, color=COLOR_TEXT)
        set_cell_background(tbl.rows[r_idx].cells[0], "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
        set_cell_background(tbl.rows[r_idx].cells[1], "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")

    doc.add_page_break()

    # -------------------------------------------------------------
    # EXECUTIVE SUMMARY & PRESENTATION INDEX
    # -------------------------------------------------------------
    add_heading_1(doc, "PRESENTATION EXECUTIVE SUMMARY & SLIDE INDEX", space_before=10)
    add_body_p(doc, "This comprehensive document serves as the official companion to the 12-slide presentation delivered for the Summer Internship Program (SIP) evaluation at Universal AI University. It contains the exact slide layouts, detailed bullet text, embedded architectural diagrams, performance metrics, and the formal oral presentation defense scripts prepared for faculty evaluators.")
    
    # Slide index table
    idx_tbl = doc.add_table(rows=13, cols=3)
    idx_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(idx_tbl, color="CBD5E1", sz="4")
    idx_col_w = [Inches(1.0), Inches(4.3), Inches(1.5)]
    for row in idx_tbl.rows:
        for idx, w in enumerate(idx_col_w):
            row.cells[idx].width = w

    headers = ["Slide #", "Slide Title / Topic", "Category"]
    for idx, h in enumerate(headers):
        format_cell(idx_tbl.rows[0].cells[idx], h, bold=True, font_size=9.5, color=RGBColor(0xFF, 0xFF, 0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_background(idx_tbl.rows[0].cells[idx], "1E3A8A")

    slides_index = [
        ("Slide 1", "Summer Internship Program Evaluation (Cover Slide)", "Candidate Details"),
        ("Slide 2", "Company / Organization Overview", "Institutional Context"),
        ("Slide 3", "Internship Objectives", "Strategic Goals"),
        ("Slide 4", "Roles & Responsibilities", "Engineering Scope"),
        ("Slide 5", "Project Overview & Problem Statement", "Ecosystem Definition"),
        ("Slide 6", "Technologies & Tools Used", "Full-Stack Tech Stack"),
        ("Slide 7", "Methodology & Development Workflow", "Agile SDLC Stages"),
        ("Slide 8", "System Architecture & Data Model", "ER & State Machine"),
        ("Slide 9", "Key Contributions & Achievements", "Technical Deliverables"),
        ("Slide 10", "Key Challenges & Engineering Solutions", "Problem Solving"),
        ("Slide 11", "Results & Impact Benchmarks", "Empirical Evaluation"),
        ("Slide 12", "Future Scope & Strategic Recommendations", "Roadmap & Scaling")
    ]
    for r_idx, (s_no, s_title, s_cat) in enumerate(slides_index):
        row = idx_tbl.rows[r_idx + 1]
        format_cell(row.cells[0], s_no, bold=True, font_size=9.0, align=WD_ALIGN_PARAGRAPH.CENTER, color=COLOR_NAVY)
        format_cell(row.cells[1], s_title, bold=False, font_size=9.0)
        format_cell(row.cells[2], s_cat, bold=False, font_size=9.0, align=WD_ALIGN_PARAGRAPH.CENTER)
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        set_cell_background(row.cells[0], bg)
        set_cell_background(row.cells[1], bg)
        set_cell_background(row.cells[2], bg)

    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 1
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 1: SUMMER INTERNSHIP PROGRAM EVALUATION", space_before=10)
    add_body_p(doc, "Slide Type: Title / Cover Slide | Visual Style: Centered Evaluation Header with Candidate & Mentorship Grid Cards.")
    
    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Evaluation Header: ", "SUMMER INTERNSHIP PROGRAM EVALUATION")
    add_bullet_item(doc, "Candidate Details: ", "Himanshu Pathak | UID: UAI05BT12417 | Batch: 2024-28 (Semester 4)")
    add_bullet_item(doc, "Internship Role: ", "Full-Stack AI & Clinical Assessment Systems Intern")
    add_bullet_item(doc, "Host Organization: ", "AI Cell, Universal AI University (4th May 2026 - 13th June 2026)")
    add_bullet_item(doc, "Mentorship Grid: ", "Internal Faculty Guide: Prof. Rajesh Bhise | Head of Department: Dr. Shivaji Pawar")
    add_bullet_item(doc, "Project Title: ", "Full-Stack AI & Clinical Assessment Systems: Engineering the UAi PsychePortal Suite & ProductivAI")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "Good morning respected internal faculty guide Prof. Rajesh Bhise, Head of Department Dr. Shivaji Pawar, and esteemed panel members. "
        "My name is Himanshu Pathak, Roll No UAI05BT12417, from the B-Tech AI and Machine Learning batch of 2024 to 2028. "
        "Today, I am proud to present the work I completed during my six-week Summer Internship Program at the AI Cell, Universal AI University, entitled: "
        "'Full-Stack AI and Clinical Assessment Systems: Engineering the UAi PsychePortal Integrated Suite and ProductivAI Analytics Engine'."
    )
    
    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("What was your primary mandate during this 6-week internship tenure at the AI Cell?",
         "My mandate was to design, implement, and deploy a dual-service production software platform that eliminates paper-based delays in campus mental health screening using standardized clinical algorithms, while simultaneously training a machine learning engine that correlates daily lifestyle habits with student academic productivity.")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 2
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 2: COMPANY / ORGANIZATION OVERVIEW", space_before=10)
    add_body_p(doc, "Slide Type: Context & Profile | Visual Style: Dual-Card Layout with Left Institutional Profile & Right Official Crest Logo.")
    
    add_figure(doc, LOGO_IMG, "Figure 2.1 – Universal AI University Official Institutional Crest", width_inches=3.0)

    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Mission Tagline: ", "Transforming institutional student wellness and productivity through automated clinical intelligence and predictive AI.")
    add_bullet_item(doc, "Parent Institution: ", "AI Cell, Universal AI University (Established under Maharashtra Act No. III of 2023; recognized by UGC).")
    add_bullet_item(doc, "Institutional Distinction: ", "India's 1st AI University dedicated to cutting-edge AI, Machine Learning, and future technology engineering.")
    add_bullet_item(doc, "Core Engineering Team: ", "School of AI & Future Technologies (Interdisciplinary hub bridging clinical psychometrics, machine learning, and scalable web engineering).")
    add_bullet_item(doc, "Operational Mandate: ", "Develops production software for campus operations, student health, and lifestyle tracking, engineering robust data pipelines, standardized diagnostic tools, and predictive ML systems.")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "To set the context: The AI Cell at Universal AI University operates as a specialized incubation hub dedicated to building production-ready, data-driven systems. "
        "Within the School of AI & Future Technologies, our focus spans high-throughput data engineering, applied machine learning, and human-centric software. "
        "In higher education, student mental health and cognitive burnout represent critical institutional challenges. "
        "Our mission was to move beyond isolated academic research and engineer real-world software that provides campus counsellors with instantaneous diagnostic intelligence."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("Why was this project developed in-house at the university's AI Cell rather than procuring a commercial SaaS tool?",
         "Commercial psychometric platforms are generic, expensive, store sensitive student psychological records on external commercial servers, and fail to integrate with university counselling workflows. By engineering the platform in-house, we maintained 100% data sovereignty, adhered to strict role-based clinical confidentiality, and customized the triage logic to our exact institutional norms.")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 3
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 3: INTERNSHIP OBJECTIVES", space_before=10)
    add_body_p(doc, "Slide Type: Objectives & Deliverables | Visual Style: 3 Rounded Cards with Standardized Metric Icons.")

    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Objective 1 – Standardized Clinical Ingestion: ", "Build a zero-friction, mobile-responsive standalone web intake portal operating on Port 5001 for standardized psychometric assessments (DASS-21, BFI-44, EQ/SQ) without authentication barriers.")
    add_bullet_item(doc, "Objective 2 – Real-Time Risk State Machine: ", "Implement exact mathematical reverse scoring (6 - R formulation) and real-time event-driven crisis triggers that immediately elevate Severe and Moderate student psychological distress to counsellors.")
    add_bullet_item(doc, "Objective 3 – Predictive Lifestyle Analytics: ", "Train and serve a Scikit-Learn regression pipeline (ProductivAI) to predict daily student productivity scores (0-100) and generate automated, rule-based behavioral interventions.")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "We structured our engineering objectives around three pillars. "
        "First, we required a frictionless web intake on Port 5001 so students could complete assessments without tedious login steps that cause high drop-off rates. "
        "Second, we needed 100% mathematical fidelity in computing psychometric scores—including complex reverse-keyed items—and triggering instant crisis alerts. "
        "Third, we recognized that psychological health is directly tied to lifestyle habits; hence, we built ProductivAI to quantitatively correlate sleep, exercise, and screen time with daily cognitive productivity."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("Why separate the student survey portal from the counsellor dashboard across different ports?",
         "Separating the survey intake on Port 5001 from the administrative dashboard on Port 5000 enforces architectural decoupling and network isolation. Students access a lightweight, zero-login submission endpoint that cannot access administrative or other students' records, while counsellors operate within a secure, authenticated React SPA on Port 5000.")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 4
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 4: ROLES & RESPONSIBILITIES", space_before=10)
    add_body_p(doc, "Slide Type: Ownership & Work Breakdown | Visual Style: 4 Numbered Vertical Domain Cards.")

    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Domain 1 – Backend Architecture & Relational Modeling: ", "Designed normalized relational schemas in SQLAlchemy ORM for Users, Profiles, Scores, and RiskAlerts across SQLite (WAL mode) and PostgreSQL.")
    add_bullet_item(doc, "Domain 2 – Clinical Scoring & Crisis Alert Pipeline: ", "Implemented standardized formulations for DASS-21, BFI-44 (6-R reverse keying), and automated server-side event triggers for immediate crisis triage.")
    add_bullet_item(doc, "Domain 3 – SPA Frontend & ReportLab PDF Engine: ", "Built 11 React SPA dashboard views using Vite and TailwindCSS, and programmed dynamic ReportLab multi-page clinical diagnostic PDF generators.")
    add_bullet_item(doc, "Domain 4 – Machine Learning & Systems Orchestration: ", "Trained Random Forest regressors (R^2 = 0.912) on 50k samples served via FastAPI (Port 8000), and authored multi-process Windows launcher scripts.")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "As the lead full-stack AI intern, my responsibilities spanned the entire software development lifecycle. "
        "On the backend, I designed 3NF relational schemas using SQLAlchemy ORM to manage multi-tiered psychometric evaluations. "
        "I wrote the mathematical scoring algorithms in Python, ensuring every reverse-coded Likert item strictly adhered to clinical literature. "
        "On the frontend, I constructed the Single Page Application using React 18 and Vite. "
        "Additionally, I managed the ML lifecycle: generating a 50k dataset, training Random Forest estimators, and serving real-time predictions via FastAPI."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("Did you work as part of a team or deliver these components independently?",
         "I engineered and owned the core full-stack codebase—spanning the Flask app factory, SQLAlchemy schema, scoring engine, React SPA views, ReportLab PDF builders, and FastAPI ML service—under the academic supervision and architectural guidance of Prof. Rajesh Bhise.")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 5
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 5: PROJECT OVERVIEW & PROBLEM STATEMENT", space_before=10)
    add_body_p(doc, "Slide Type: Problem & Solution Definition | Visual Style: Problem Statement Callout + 4 Feature Cards with Checkpoint Icons.")

    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Elevator Pitch: ", "Dual-service production ecosystem unifying clinical psychological assessment with machine learning lifestyle analytics.")
    add_bullet_item(doc, "Problem Statement: ", "\"Higher education institutions suffer from 3-14 day delays and error-prone manual reverse scoring in student mental health screening, with zero empirical correlation to daily lifestyle habits.\"")
    add_bullet_item(doc, "Key Feature 1 (Zero-Friction Ingestion): ", "Mobile-responsive standalone web intake running on Port 5001 for immediate questionnaire completion.")
    add_bullet_item(doc, "Key Feature 2 (Automated Scoring & Risk Engine): ", "Exact DASS-21 scaling, BFI-44 (6 - R) reverse keying, and instant crisis flags.")
    add_bullet_item(doc, "Key Feature 3 (Programmatic Clinical Dossiers): ", "Dynamic ReportLab PDF rendering compiling complete clinical reports in under 850 milliseconds.")
    add_bullet_item(doc, "Key Feature 4 (ProductivAI ML Analytics): ", "FastAPI engine predicting productivity (0-100) from sleep quality, study hours, exercise, screen time, and mood.")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "Slide 5 articulates the fundamental problem our software resolves. "
        "In universities, psychological screening is typically handled via paper forms. "
        "Students fill them out, counsellors collect them, and manually grade them. "
        "This introduces a 3 to 14 day delay. If a student is suffering from severe depression or acute anxiety, a two-week delay can be dangerous. "
        "Furthermore, human evaluators frequently miscalculate reverse-scored questions. "
        "Our system eliminates this: tests are scored in 12 milliseconds, crisis cases trigger emergency dashboard alerts in 28 milliseconds, and comprehensive PDF dossiers are generated in 850 milliseconds."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("What exactly is reverse scoring and why does it cause manual errors?",
         "In validated psychological inventories like the Big Five (BFI-44), certain questions are phrased negatively to prevent acquiescence bias. For instance, in measuring Conscientiousness, an item like 'Can be somewhat careless' must be inverted on a 5-point scale using 6 - R. Manual reviewers or basic Excel formulas frequently forget to apply this inversion, completely invalidating the student's psychological profile.")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 6
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 6: TECHNOLOGIES & TOOLS USED", space_before=10)
    add_body_p(doc, "Slide Type: Tech Stack Matrix | Visual Style: 6 Symmetrical Category Cards with Vector Technology Icons.")

    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Frontend / Interface: ", "React 18, Vite 5, TailwindCSS 3.4, Chart.js 4.4, Lucide-React")
    add_bullet_item(doc, "Core Backend: ", "Python 3.13, Flask 3.0.0 (Application Factory Pattern), FastAPI 0.109+")
    add_bullet_item(doc, "Database & Storage: ", "Flask-SQLAlchemy 3.1, SQLite (WAL Mode), PostgreSQL 15, Alembic")
    add_bullet_item(doc, "AI & Machine Learning: ", "Scikit-Learn 1.3 (Random Forest Regressor), Pandas 2.1, NumPy, Joblib")
    add_bullet_item(doc, "Authentication & Security: ", "Flask-Login, Flask-Bcrypt, Flask-WTF (CSRF), HTTP-only Signed Cookies")
    add_bullet_item(doc, "Reporting & DevOps: ", "ReportLab 4.1 (PDF Engine), OpenPyXL, PowerShell & Batch Process Launchers")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "Our technology stack was deliberately chosen for performance, security, and developer ergonomics. "
        "For client interfaces, we chose React 18 bundled with Vite and styled with TailwindCSS for ultra-fast rendering. "
        "On the backend, Flask manages authentication, administrative routing, and relational persistence via SQLAlchemy. "
        "For machine learning, we deployed FastAPI alongside Scikit-Learn because FastAPI provides asynchronous request handling and sub-15ms inference latency. "
        "ReportLab was integrated for server-side PDF document generation, and Bcrypt with HTTP-only cookies guarantees enterprise-grade security."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("Why use both Flask and FastAPI instead of standardizing on one framework?",
         "Flask is mature, stable, and offers rich ecosystem plugins like Flask-Login, Flask-Bcrypt, and Flask-WTF for complex session-based administrative web applications. FastAPI, on the other hand, is built on Starlette and Pydantic, offering native asynchronous endpoints and automated OpenAPI docs, making it the ideal runtime for low-latency machine learning inference in ProductivAI.")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 7
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 7: METHODOLOGY & WORKFLOW", space_before=10)
    add_body_p(doc, "Slide Type: SDLC Methodology | Visual Style: 4 Linear Stages on Left + Embedded Methodology Flow Diagram on Right.")

    add_figure(doc, FIG1_1, "Figure 7.1 – Four-Stage Development Methodology Flowchart", width_inches=5.8)

    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Phase 1 – Requirements & Domain Analysis: ", "Analyzed Lovibond DASS-21 and John & Srivastava BFI-44 clinical norms; mapped mathematical scoring formulations and cutoffs.")
    add_bullet_item(doc, "Phase 2 – Relational Architecture & Modeling: ", "Designed normalized 3NF database schema, decoupled microservices, and established typed RESTful API contracts.")
    add_bullet_item(doc, "Phase 3 – Core Implementation & ML Training: ", "Built app/scoring.py, ReportLab PDF generators, and trained Random Forest regressors on 50,000 synthetic lifestyle rows.")
    add_bullet_item(doc, "Phase 4 – Integration, Testing & Deployment: ", "Developed React SPA views, executed multi-tiered testing suites, and authored automated launch_all orchestrators.")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "We adopted an Agile, Component-Driven, and API-First development methodology divided into four sequential stages as illustrated in Figure 7.1. "
        "In Phase 1, we analyzed validated clinical psychometrics to derive exact normative ranges. "
        "In Phase 2, we drafted third-normal-form entity schemas and decoupled backend services. "
        "In Phase 3, we wrote the mathematical algorithms, integrated ReportLab flowables, and trained our Random Forest regression models. "
        "Finally, in Phase 4, we built the React frontend, executed unit and load testing, and automated multi-process deployment."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("How did you ensure clinical validity during Phase 1?",
         "We referenced primary clinical literature: Lovibond & Lovibond (1995) for DASS-21 item distributions and scoring multipliers, John & Srivastava (1999) for the 44-item Big Five Inventory with exact reverse-item matrices, and Baron-Cohen for EQ/SQ cognitive profiles, validating our formulas against published benchmark tables.")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 8
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 8: SYSTEM ARCHITECTURE & DATA MODEL", space_before=10)
    add_body_p(doc, "Slide Type: Architectural Blueprints | Visual Style: Dual Diagram Split with ER Diagram on Left & State Machine on Right.")

    add_figure(doc, FIG1_2, "Figure 8.1 – Relational Entity-Relationship Diagram (SQLAlchemy ORM)", width_inches=5.8)
    add_figure(doc, FIG1_3, "Figure 8.2 – Deterministic Clinical Scoring & Risk State Machine", width_inches=5.8)

    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Architectural Philosophy: ", "Multi-service relational architecture with automated lead triage and clinical risk state machines.")
    add_bullet_item(doc, "Entity-Relationship Model (Figure 8.1): ", "Six normalized core tables: User, StudentProfile, Assessment, SubscaleScore, RiskAlert, and ProductivityLog with foreign key integrity and cascade constraints.")
    add_bullet_item(doc, "Clinical State Machine (Figure 8.2): ", "Deterministic 5-state lifecycle: Intake (Port 5001) -> Scoring Engine (6-R Matrix) -> Threshold Evaluation -> Emergency Crisis Alert vs Normal Archive -> ReportLab PDF Build.")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "Slide 8 illustrates the technical backbone of our system. "
        "On the left, Figure 8.1 shows our Entity-Relationship schema: User credentials link to StudentProfiles with a 1-to-1 relationship, while each profile connects to multiple Assessments, SubscaleScores, and RiskAlerts. "
        "On the right, Figure 8.2 shows the Clinical State Machine. When a student submits a survey, it is parsed, scored, and reverse-keyed. "
        "If any subscale score meets or exceeds clinical severity cutoffs (such as DASS-21 Depression > 14 or Anxiety > 10), the system transitions to an Emergency Alert state, broadcasting a flashing red notification to the Counsellor Dashboard."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("What database concurrency mode did you use to prevent race conditions during simultaneous student submissions?",
         "We enabled SQLite WAL (Write-Ahead Logging) mode (`PRAGMA journal_mode=WAL`), which permits concurrent readers while maintaining atomic single-writer locks. Furthermore, each assessment submission is executed within an atomic SQLAlchemy database transaction (`db.session.commit()` with automated `rollback()` on exception).")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 9
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 9: KEY CONTRIBUTIONS & ACHIEVEMENTS", space_before=10)
    add_body_p(doc, "Slide Type: Engineering Milestones | Visual Style: 5 Numbered Highlight Cards with Bold Headings.")

    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Achievement 1 – Dual-Service Production Ecosystem: ", "Architected, developed, and deployed UAi PsychePortal (Ports 5000/5001) and ProductivAI ML engine (Port 8000) in 6 weeks.")
    add_bullet_item(doc, "Achievement 2 – Zero Crisis Window Latency: ", "Eliminated 3-14 day manual triage delays by triggering automated emergency risk alerts in under 28 milliseconds.")
    add_bullet_item(doc, "Achievement 3 – 100% Algorithmic Scoring Fidelity: ", "Implemented flawless DASS-21 subscale math and BFI-44 6-R reverse scoring verified across comprehensive test suites.")
    add_bullet_item(doc, "Achievement 4 – Automated Clinical Dossier Generation: ", "Built dynamic ReportLab PDF generator compiling multi-page diagnostic records in under 850ms, saving 40 minutes per student evaluation.")
    add_bullet_item(doc, "Achievement 5 – High-Precision ML Productivity Model: ", "Trained Random Forest Regressor achieving R^2 = 0.912 and MAE = 3.42, served via FastAPI with sub-15ms inference latency.")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "Slide 9 highlights our five key engineering deliverables. "
        "First, we delivered a dual-service architecture that spans clinical health and productivity. "
        "Second, we reduced institutional emergency response time from weeks to milliseconds. "
        "Third, we attained 100% computational fidelity on psychological scoring rubrics. "
        "Fourth, our dynamic ReportLab generator saves counsellors roughly 40 minutes of manual paperwork per student. "
        "Fifth, our machine learning model achieved an exceptional R-squared score of 0.912, providing students with accurate habit interventions."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("How did you calculate the 40 minutes saved per student evaluation?",
         "In standard practice, a campus counsellor spends 15-20 minutes manually calculating item scores and reverse keys, 10 minutes cross-referencing normative lookup tables, and 15 minutes typing a diagnostic clinical summary report. Our system automates calculation, norm lookup, and PDF report compilation in under one second, eliminating 40 minutes of administrative overhead per case.")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 10
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 10: KEY CHALLENGES & ENGINEERING SOLUTIONS", space_before=10)
    add_body_p(doc, "Slide Type: Problem Solving Matrix | Visual Style: Two-Column Side-by-Side Comparison (Red Challenges vs. Green Solutions).")

    # Table layout
    c_tbl = doc.add_table(rows=4, cols=2)
    c_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(c_tbl, color="CBD5E1", sz="4")
    c_col_w = [Inches(3.3), Inches(3.3)]
    for row in c_tbl.rows:
        for idx, w in enumerate(c_col_w):
            row.cells[idx].width = w

    format_cell(c_tbl.rows[0].cells[0], "Key Challenges Encountered", bold=True, font_size=10.0, color=RGBColor(0xFF, 0xFF, 0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_background(c_tbl.rows[0].cells[0], "EF4444")
    format_cell(c_tbl.rows[0].cells[1], "Applied Engineering Solutions", bold=True, font_size=10.0, color=RGBColor(0xFF, 0xFF, 0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_background(c_tbl.rows[0].cells[1], "16A34A")

    challenges_data = [
        ("1. Cyclic Imports & Blueprint Decoupling:\nTight coupling between SQLAlchemy models, authentication blueprints, and route handlers causing circular import errors upon initialization.",
         "Implemented the Flask Application Factory pattern (create_app), isolating model declarations and extensions from route handlers."),
        ("2. Reverse Keying & Missing Item Failures:\nMissing survey inputs or manual inversions crashing matrix subscale calculations during submission.",
         "Engineered safe dictionary lookups with neutral default imputation (3 for BFI, 0 for DASS) and automated 6 - R mathematical transforms."),
        ("3. Multi-Service Port Orchestration:\nManaging concurrent execution and port collisions across microservices on ports 5000, 5001, and 8000.",
         "Authored unified PowerShell & Batch scripts (launch_all.bat) with automated port-availability checks and background process management.")
    ]
    for r_idx, (ch, sol) in enumerate(challenges_data):
        row = c_tbl.rows[r_idx + 1]
        format_cell(row.cells[0], ch, bold=False, font_size=9.0)
        format_cell(row.cells[1], sol, bold=False, font_size=9.0)
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        set_cell_background(row.cells[0], bg)
        set_cell_background(row.cells[1], bg)

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes", space_before=12)
    add_speaker_script_box(doc, 
        "Engineering complex distributed applications inevitably introduces architectural roadblocks. "
        "Our first challenge was circular dependencies in Flask. We resolved this by implementing the Application Factory pattern, ensuring models are registered before blueprints are bound. "
        "Our second challenge was survey data integrity—if a student skipped an item, simple matrix summation crashed. We solved this with safe dictionary lookups and neutral fallback imputation. "
        "Our third challenge was orchestrating three distinct servers. We authored launch_all.bat to automate port scanning, virtual environment activation, and multi-process startup in a single click."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("What happens if Port 5000 or 8000 is already in use when launch_all is executed?",
         "The PowerShell orchestrator executes `Get-NetTCPConnection` to inspect port bindings prior to spawning workers. If a port conflict is detected, it terminates the stale zombie process or logs a clear diagnostic alert to the terminal before initializing the application.")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 11
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 11: RESULTS & IMPACT BENCHMARKS", space_before=10)
    add_body_p(doc, "Slide Type: Empirical Benchmarking | Visual Style: Quantitative Subtitles + Full-Width Embedded Benchmark Dashboard.")

    add_figure(doc, FIG_BENCHMARK, "Figure 11.1 – Measured Subsystem Latency vs. Target SLA & Clinical Impact Cards", width_inches=6.0)

    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Latency Subtitle: ", "Sub-15ms ML inference, 12ms clinical scoring, and 850ms dynamic PDF dossier generation.")
    add_bullet_item(doc, "Impact Subtitle: ", "Reduced institutional crisis identification time from 14 days to real time, saving counsellors 40 minutes per evaluation.")
    add_bullet_item(doc, "Survey Intake Latency: ", "Measured: 85 ms | Target SLA: < 250 ms | Status: PASSED (66% faster)")
    add_bullet_item(doc, "Clinical Scoring Execution: ", "Measured: 12 ms | Target SLA: < 50 ms | Status: PASSED (76% faster)")
    add_bullet_item(doc, "Emergency Risk Trigger: ", "Measured: 28 ms | Target SLA: < 100 ms | Status: PASSED (72% faster)")
    add_bullet_item(doc, "ReportLab PDF Generation: ", "Measured: 850 ms | Target SLA: < 2000 ms | Status: PASSED (58% faster)")
    add_bullet_item(doc, "FastAPI ML Model Inference: ", "Measured: 14 ms | Target SLA: < 50 ms | Status: PASSED (72% faster)")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "Slide 11 presents our measured empirical performance benchmarks, illustrated in Figure 11.1. "
        "Across every critical subsystem, our measured performance substantially outperformed our target Service Level Agreements. "
        "Survey submissions process in 85 milliseconds. Psychological scoring runs in 12 milliseconds. "
        "Emergency crisis alerts broadcast in 28 milliseconds. "
        "Dynamic PDF generation completes in 850 milliseconds, and machine learning inference takes just 14 milliseconds. "
        "Most importantly, this technology eliminates 99.9% of triage latency, ensuring campus counsellors can intervene before a crisis escalates."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("How did you measure these latency figures?",
         "We used Python's `time.perf_counter_ns()` decorator across internal function calls and executed Apache Benchmark (`ab`) and Postman collection runners to measure HTTP round-trip latency over 1,000 requests, calculating median and 95th-percentile response timings.")
    ])
    doc.add_page_break()

    # -------------------------------------------------------------
    # SLIDE 12
    # -------------------------------------------------------------
    add_heading_1(doc, "SLIDE 12: FUTURE SCOPE & STRATEGIC RECOMMENDATIONS", space_before=10)
    add_body_p(doc, "Slide Type: Strategic Roadmap | Visual Style: 4 Sequential Numbered Strategic Vision Cards.")

    add_heading_2(doc, "1. Content Displayed on Slide")
    add_bullet_item(doc, "Roadmap 1 – Cloud-Native Containerization: ", "Containerize Flask, FastAPI, and React services using Docker and deploy on Kubernetes for high-availability multi-campus scaling.")
    add_bullet_item(doc, "Roadmap 2 – Cross-Platform Mobile Application: ", "Develop a native Flutter mobile client for Android and iOS to facilitate daily lifestyle tracking and emergency push notifications.")
    add_bullet_item(doc, "Roadmap 3 – Generative LLM Clinical Summaries: ", "Integrate local, HIPAA-compliant Large Language Models (LLMs) to synthesize longitudinal assessment histories into draft counsellor consultation notes.")
    add_bullet_item(doc, "Roadmap 4 – Continuous ML Model Retraining: ", "Implement automated MLOps retraining pipelines to continually adapt the Random Forest productivity model based on verified end-of-semester student academic GPAs.")

    add_heading_2(doc, "2. Speaker Delivery & Defense Notes")
    add_speaker_script_box(doc, 
        "To conclude, our future development roadmap focuses on scalability, accessibility, and AI enhancement. "
        "First, we plan to containerize the application with Docker and Kubernetes for multi-campus university deployments. "
        "Second, we aim to build a cross-platform Flutter mobile application to empower students to log lifestyle habits effortlessly on their phones. "
        "Third, we plan to integrate privacy-first local Large Language Models to draft preliminary consultation notes for counsellors. "
        "Fourth, we will establish continuous MLOps feedback loops connecting lifestyle recommendations directly to academic GPA improvements. "
        "Thank you, mentors and panel members. I now welcome your questions."
    )

    add_heading_2(doc, "3. Defense Preparation Q&A")
    add_viva_qa_box(doc, [
        ("If you integrate an LLM for clinical notes, how will you protect student psychological confidentiality?",
         "We will deploy an open-weights LLM (such as LLaMA-3 or Mistral) locally on on-premise university infrastructure within an air-gapped environment. No student psychological evaluation or demographic data will ever leave the university firewall or be transmitted to commercial public cloud APIs.")
    ])

    # Save to workspace and downloads
    doc.save(OUT_DOCX_WS)
    shutil.copyfile(OUT_DOCX_WS, OUT_DOCX_DL)
    print(f"Successfully generated DOCX:\n1. {OUT_DOCX_WS}\n2. {OUT_DOCX_DL}")

    # Attempt PDF conversion
    try:
        import docx2pdf
        docx2pdf.convert(OUT_DOCX_WS, OUT_PDF_WS)
        shutil.copyfile(OUT_PDF_WS, OUT_PDF_DL)
        print(f"Successfully generated PDF:\n1. {OUT_PDF_WS}\n2. {OUT_PDF_DL}")
    except Exception as e:
        print(f"PDF conversion note: {e}")

if __name__ == "__main__":
    build_document()
