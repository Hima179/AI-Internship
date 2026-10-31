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

from build_exact_helpers import (
    WORKSPACE, OUTPUT_DOCX, OUTPUT_PDF, DOWNLOADS_DOCX, DOWNLOADS_PDF,
    LOGO_HEADER_IMG, WEEKLY_LOGO_IMG, STUDENT_SIGNATURE_IMG, OFFER_LETTER_IMG,
    FIG1_1, FIG1_2, FIG1_3, FIG1_4, COLOR_BLACK,
    COLOR_UNI_BLUE, COLOR_ACT_GREEN, COLOR_SCHOOL_GREEN,
    set_cell_background, set_cell_margins, set_table_borders, format_cell,
    add_heading_1, add_heading_2, add_heading_3, add_body_p, add_bullet_item, add_figure,
    configure_main_section
)

def add_weekly_header(doc):
    """Adds the official university header for weekly report pages matching Akhil Barman's reference."""
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="FFFFFF", sz="0")
    tbl.rows[0].cells[0].width = Inches(2.3)
    tbl.rows[0].cells[1].width = Inches(4.1)

    # Left cell: Logo
    p_logo = tbl.rows[0].cells[0].paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_logo.paragraph_format.space_before = Pt(0)
    p_logo.paragraph_format.space_after = Pt(0)
    if os.path.exists(WEEKLY_LOGO_IMG):
        r_l = p_logo.add_run()
        r_l.add_picture(WEEKLY_LOGO_IMG, width=Inches(2.2))

    # Right cell: University text
    p_uni = tbl.rows[0].cells[1].paragraphs[0]
    p_uni.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_uni.paragraph_format.space_before = Pt(0)
    p_uni.paragraph_format.space_after = Pt(0)
    p_uni.paragraph_format.line_spacing = 1.05
    
    r_u1 = p_uni.add_run("Universal Ai\nUniversity\n")
    r_u1.font.name = "Georgia"
    r_u1.font.size = Pt(20)
    r_u1.bold = True
    r_u1.font.color.rgb = COLOR_UNI_BLUE

    r_u2 = p_uni.add_run("Established vide Maharashtra Act No. III of 2023, of Government of Maharashtra, and\nrecognized by the UGC Act 1956.")
    r_u2.font.name = "Calibri"
    r_u2.font.size = Pt(7.5)
    r_u2.font.color.rgb = COLOR_ACT_GREEN

    p_sch = doc.add_paragraph()
    p_sch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sch.paragraph_format.space_before = Pt(3)
    p_sch.paragraph_format.space_after = Pt(4)
    r_sch = p_sch.add_run("School of Ai & Future Technologies")
    r_sch.font.name = "Cambria"
    r_sch.font.size = Pt(15.5)
    r_sch.bold = True
    r_sch.font.color.rgb = COLOR_SCHOOL_GREEN


def add_student_company_tables(doc):
    p_sd_title = doc.add_paragraph()
    p_sd_title.paragraph_format.space_before = Pt(2)
    p_sd_title.paragraph_format.space_after = Pt(2)
    r_sdt = p_sd_title.add_run("Student Details")
    r_sdt.font.name = "Times New Roman"
    r_sdt.font.size = Pt(11)
    r_sdt.bold = True

    tbl_sd = doc.add_table(rows=3, cols=2)
    tbl_sd.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_sd, color="000000", sz="3")
    for row in tbl_sd.rows:
        row.cells[0].width = Inches(3.2)
        row.cells[1].width = Inches(3.2)

    format_cell(tbl_sd.rows[0].cells[0], "Student Name: Himanshu Pathak", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl_sd.rows[0].cells[1], "Roll No.: UAI05BT12417", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl_sd.rows[1].cells[0], "Year/ Semester: 4th semester", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl_sd.rows[1].cells[1], "Email Id: himanshu.pathak@universalai.in", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl_sd.rows[2].cells[0], "Faculty Mentor : Prof. Rajesh Bhise", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl_sd.rows[2].cells[1], "Contact No.: 9820767182", bold=True, font_name="Times New Roman", font_size=10.5)

    p_cd_title = doc.add_paragraph()
    p_cd_title.paragraph_format.space_before = Pt(4)
    p_cd_title.paragraph_format.space_after = Pt(2)
    r_cdt = p_cd_title.add_run("Company Details:")
    r_cdt.font.name = "Times New Roman"
    r_cdt.font.size = Pt(11)
    r_cdt.bold = True

    tbl_cd = doc.add_table(rows=3, cols=2)
    tbl_cd.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_cd, color="000000", sz="3")
    for row in tbl_cd.rows:
        row.cells[0].width = Inches(3.2)
        row.cells[1].width = Inches(3.2)

    format_cell(tbl_cd.rows[0].cells[0], "Company Name: Ai Cell, Universal Ai University", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl_cd.rows[0].cells[1], "Department Name: School of Ai & Future Technologies", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl_cd.rows[1].cells[0], "Company Manger Name: Prof. Rajesh Bhise / Dr. Shivaji Pawar", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl_cd.rows[1].cells[1], "Official Mail Id:\naicell@universalai.in", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl_cd.rows[2].cells[0], "Contact No: +91 2192 664000", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl_cd.rows[2].cells[1], "Website: https://www.universalai.in", bold=True, font_name="Times New Roman", font_size=10.5)

    p_proj = doc.add_paragraph()
    p_proj.paragraph_format.space_before = Pt(4)
    p_proj.paragraph_format.space_after = Pt(2)
    r_pr = p_proj.add_run("Project Title: Full-Stack AI & Clinical Assessment Systems (UAi PsychePortal & ProductivAI)")
    r_pr.font.name = "Times New Roman"
    r_pr.font.size = Pt(11.5)
    r_pr.bold = True

def add_weekly_meta(doc, week_str, period_str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f"Week No.: {week_str}\nReporting Period: {period_str}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

def add_task_table(doc, tasks):
    p_wt_title = doc.add_paragraph()
    p_wt_title.paragraph_format.space_before = Pt(3)
    p_wt_title.paragraph_format.space_after = Pt(2)
    r_wtt = p_wt_title.add_run("1. Weekly Task")
    r_wtt.font.name = "Times New Roman"
    r_wtt.font.size = Pt(12)
    r_wtt.bold = True

    tbl = doc.add_table(rows=len(tasks) + 1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="000000", sz="3")
    for row in tbl.rows:
        row.cells[0].width = Inches(0.6)
        row.cells[1].width = Inches(4.8)
        row.cells[2].width = Inches(1.1)

    format_cell(tbl.rows[0].cells[0], "S. No", bold=True, font_name="Times New Roman", font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(tbl.rows[0].cells[1], "Task Description", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl.rows[0].cells[2], "Status", bold=True, font_name="Times New Roman", font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    for idx, (desc, status) in enumerate(tasks):
        row = tbl.rows[idx + 1]
        format_cell(row.cells[0], str(idx + 1), font_name="Times New Roman", font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(row.cells[1], desc, font_name="Times New Roman", font_size=10)
        format_cell(row.cells[2], status, font_name="Times New Roman", font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)

def add_tech_tools(doc, tools):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run("2. Technologies/Tools Used")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    for item in tools:
        add_bullet_item(doc, "", item, space_after=1)

def add_learning_outcomes(doc, outcomes):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run("3. Learning Outcomes")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    for item in outcomes:
        add_bullet_item(doc, "", item, space_after=1)

def add_challenges_solutions(doc, challenges, solutions):
    p_ch = doc.add_paragraph()
    p_ch.paragraph_format.space_before = Pt(3)
    p_ch.paragraph_format.space_after = Pt(1)
    r_ch = p_ch.add_run("4. Challenges Faced & Solutions")
    r_ch.font.name = "Times New Roman"
    r_ch.font.size = Pt(12)
    r_ch.bold = True

    p_c_lbl = doc.add_paragraph()
    p_c_lbl.paragraph_format.space_before = Pt(1)
    p_c_lbl.paragraph_format.space_after = Pt(1)
    r_cl = p_c_lbl.add_run("Challenges:")
    r_cl.font.name = "Times New Roman"
    r_cl.font.size = Pt(11)
    r_cl.bold = True
    for item in challenges:
        add_bullet_item(doc, "", item, space_after=1)

    p_s_lbl = doc.add_paragraph()
    p_s_lbl.paragraph_format.space_before = Pt(2)
    p_s_lbl.paragraph_format.space_after = Pt(1)
    r_sl = p_s_lbl.add_run("Solutions:")
    r_sl.font.name = "Times New Roman"
    r_sl.font.size = Pt(11)
    r_sl.bold = True
    for item in solutions:
        add_bullet_item(doc, "", item, space_after=1)

def add_plan_table(doc, plans):
    p_pt = doc.add_paragraph()
    p_pt.paragraph_format.space_before = Pt(3)
    p_pt.paragraph_format.space_after = Pt(2)
    r_pt = p_pt.add_run("5. Plan for Next Week")
    r_pt.font.name = "Times New Roman"
    r_pt.font.size = Pt(12)
    r_pt.bold = True

    tbl = doc.add_table(rows=len(plans) + 1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="000000", sz="3")
    for row in tbl.rows:
        row.cells[0].width = Inches(0.6)
        row.cells[1].width = Inches(4.8)
        row.cells[2].width = Inches(1.1)

    format_cell(tbl.rows[0].cells[0], "S. No", bold=True, font_name="Times New Roman", font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(tbl.rows[0].cells[1], "Task to be done", bold=True, font_name="Times New Roman", font_size=10.5)
    format_cell(tbl.rows[0].cells[2], "Estimated Time", bold=True, font_name="Times New Roman", font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    for idx, (task, time_est) in enumerate(plans):
        row = tbl.rows[idx + 1]
        format_cell(row.cells[0], str(idx + 1), font_name="Times New Roman", font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(row.cells[1], task, font_name="Times New Roman", font_size=10)
        format_cell(row.cells[2], time_est, font_name="Times New Roman", font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)

def main():
    print("=" * 70)
    print("GENERATING EXACT UNIVERSITY FORMAT SIP HANDBOOK (43 PAGES)")
    print("=" * 70)

    doc = docx.Document()

    # Configure Section 1 (Main Report: Pages 1 to 30)
    sec1 = doc.sections[0]
    configure_main_section(sec1)

    # -----------------------------------------------------------------------
    # PAGE 1 (Numbered 2): DECLARATION BY THE CANDIDATE
    # -----------------------------------------------------------------------
    print("Writing Page 1 (Numbered 2): Declaration...")
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(28)
    p_title.paragraph_format.space_after = Pt(18)
    r = p_title.add_run("DECLARATION BY THE CANDIDATE")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = COLOR_BLACK

    add_body_p(
        doc,
        "I Himanshu Pathak hereby certify that the work which is being presented in this Summer "
        "Internship Program Report entitled \"Full-Stack AI & Clinical Assessment Systems: Engineering "
        "the UAi PsychePortal Integrated Suite and ProductivAI Analytics Engine\" in partial fulfilment "
        "of the requirement for the award of the B. Tech and submitted to the Universal AI University, Karjat "
        "is an authentic record of my own work carried out during a period from 4th May till 14th July 2026 at "
        "AI Cell, Universal AI University (name of the organization) under the guidance of Prof. Rajesh Bhise "
        "(Name and Designation of Faculty Guide).",
        space_after=10
    )
    add_body_p(
        doc,
        "The matter presented in this project report has not been submitted by me for the award of any other "
        "degree of this or any other Institute.",
        space_after=10
    )
    add_body_p(
        doc,
        "Wherever references have been made to intellectual properties of any individual / Institution / "
        "Government / Private / Public Bodies / Universities, research paper, text books, reference books, "
        "research monographs, archives of newspapers, corporate, individuals, business / Government and any other "
        "source of intellectual properties viz., speeches, quotations, conference proceedings, extracts from the "
        "website, working paper, seminal work et al, they have been clearly indicated, duly acknowledged and included "
        "in the Bibliography.",
        space_after=28
    )

    p_sig1 = doc.add_paragraph()
    p_sig1.paragraph_format.space_after = Pt(2)
    r_s1 = p_sig1.add_run("Name of the learner: Himanshu Pathak\nSignature of the Student:\n")
    r_s1.font.name = "Times New Roman"
    r_s1.font.size = Pt(12)
    r_s1.bold = True
    r_s1.font.color.rgb = COLOR_BLACK
    if os.path.exists(STUDENT_SIGNATURE_IMG):
        r_sig_img = p_sig1.add_run()
        r_sig_img.add_picture(STUDENT_SIGNATURE_IMG, width=Inches(1.5))

    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.space_before = Pt(36)
    p_cert.paragraph_format.space_after = Pt(16)
    r_c = p_cert.add_run("This is to certify that the above statement made by the candidate is correct to the best of our knowledge.")
    r_c.font.name = "Times New Roman"
    r_c.font.size = Pt(12)
    r_c.font.color.rgb = COLOR_BLACK

    p_sig2 = doc.add_paragraph()
    p_sig2.paragraph_format.space_after = Pt(0)
    r_s2 = p_sig2.add_run("Signature of Faculty Guide: ___________________________")
    r_s2.font.name = "Times New Roman"
    r_s2.font.size = Pt(12)
    r_s2.bold = True
    r_s2.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 2 (Numbered 3): OFFER LETTER
    # -----------------------------------------------------------------------
    print("Writing Page 2 (Numbered 3): Offer Letter...")
    p_ol = doc.add_paragraph()
    p_ol.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ol.paragraph_format.space_before = Pt(10)
    p_ol.paragraph_format.space_after = Pt(10)
    r_ol = p_ol.add_run("OFFER LETTER")
    r_ol.font.name = "Times New Roman"
    r_ol.font.size = Pt(14)
    r_ol.bold = True
    r_ol.font.color.rgb = COLOR_BLACK

    if os.path.exists(OFFER_LETTER_IMG):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(0)
        r_img = p_img.add_run()
        r_img.add_picture(OFFER_LETTER_IMG, width=Inches(5.4))

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 3 (Numbered 4): CERTIFICATE
    # -----------------------------------------------------------------------
    print("Writing Page 3 (Numbered 4): Certificate...")
    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_title.paragraph_format.space_before = Pt(20)
    p_cert_title.paragraph_format.space_after = Pt(18)
    r_ct = p_cert_title.add_run("CERTIFICATE")
    r_ct.font.name = "Times New Roman"
    r_ct.font.size = Pt(14)
    r_ct.bold = True
    r_ct.font.color.rgb = COLOR_BLACK

    add_body_p(
        doc,
        "This is to certify that Mr. / Ms. Himanshu Pathak is a Bonafide student at the four-year "
        "full-time School of AI and Future Technologies, BATCH 2026-27, Roll No. UAI05BT12417 "
        "of the University.",
        space_after=10
    )
    add_body_p(
        doc,
        "As a part of the University Grants Commission (UGC) guidelines, the student has "
        "carried out the Summer Internship Project Full-Stack AI & Clinical Assessment Systems: "
        "Engineering the UAi PsychePortal Integrated Suite and ProductivAI Analytics Engine "
        "(Title of the Project) at AI Cell, Universal AI University (Name of the Organization) "
        "during the period from 4th May 2026 to 14th July 2026 under my guidance in partial "
        "fulfilment of requirement for the completion B. Tech as prescribed by the University "
        "Grants Commission (UGC). This Summer Internship Program Report is the record of "
        "authentic work carried out by him / her during the period from April 2026 to July 2026.",
        space_after=40
    )

    tbl_cert = doc.add_table(rows=2, cols=2)
    tbl_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_cert, color="FFFFFF", sz="0")
    tbl_cert.rows[0].cells[0].width = Inches(3.1)
    tbl_cert.rows[0].cells[1].width = Inches(3.1)
    tbl_cert.rows[1].cells[0].width = Inches(3.1)
    tbl_cert.rows[1].cells[1].width = Inches(3.1)

    format_cell(tbl_cert.rows[0].cells[0], "Name & Signature of\n(Faculty Mentor)\nProf. Rajesh Bhise", bold=True, font_size=11, font_name="Times New Roman")
    format_cell(tbl_cert.rows[0].cells[1], "Name & Signature of\n(HOD)\nDr. Shivaji Pawar", bold=True, font_size=11, font_name="Times New Roman", align=WD_ALIGN_PARAGRAPH.RIGHT)
    format_cell(tbl_cert.rows[1].cells[0], "Place: Karjat, Mumbai\nDate: 14 July 2026", bold=False, font_size=10, font_name="Times New Roman")
    format_cell(tbl_cert.rows[1].cells[1], "School of AI & Future Technologies\nUniversal AI University", bold=False, font_size=10, font_name="Times New Roman", align=WD_ALIGN_PARAGRAPH.RIGHT)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 4 (Numbered 5): ACKNOWLEDGEMENT
    # -----------------------------------------------------------------------
    print("Writing Page 4 (Numbered 5): Acknowledgement...")
    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack.paragraph_format.space_before = Pt(20)
    p_ack.paragraph_format.space_after = Pt(16)
    r_ack = p_ack.add_run("ACKNOWLEDGEMENT")
    r_ack.font.name = "Times New Roman"
    r_ack.font.size = Pt(14)
    r_ack.bold = True
    r_ack.font.color.rgb = COLOR_BLACK

    add_body_p(
        doc,
        "It gives me immense pleasure to present this Concurrent Project Report. However, it would "
        "not have been possible without the help and support of all the team members of the AI Cell.",
        space_after=10
    )
    add_body_p(
        doc,
        "I would like to thank my Guide's Prof. Rajesh Bhise and Dr. Shivaji Pawar for guiding me in "
        "my tenure of internship on Full Stack AI Development and Clinical Assessment Systems. Without "
        "their support and guidance, I wouldn't have come so far to prepare this report.",
        space_after=10
    )
    add_body_p(
        doc,
        "I would like to express my thankfulness to Corporate Relations team of Universal Ai "
        "University, who gave me this great opportunity to work on this interesting project.",
        space_after=10
    )
    add_body_p(
        doc,
        "I am also grateful to my loving parents and my kind friends whose prayers, affection and "
        "support are always a source of encouragement. Their suggestions and supply of information "
        "were really very valuable and helpful to me. Their continuous encouragement and support "
        "helped me for completing this project successfully.",
        space_after=28
    )

    p_ack_sig = doc.add_paragraph()
    p_ack_sig.paragraph_format.space_after = Pt(0)
    r_as = p_ack_sig.add_run(
        "Name: Himanshu Pathak.\n"
        "Batch: B-Tech 2024-28\n"
        "Roll No: UAI05BT12417\n"
        "Universal AI University, Mumbai (Karjat)"
    )
    r_as.font.name = "Times New Roman"
    r_as.font.size = Pt(11)
    r_as.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 5 (Numbered 6): SUMMER INTERNSHIP PROGRAM SUBMISSION (FOR OFFICE USE ONLY)
    # -----------------------------------------------------------------------
    print("Writing Page 5 (Numbered 6): Submission Form...")
    p_sub_title = doc.add_paragraph()
    p_sub_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub_title.paragraph_format.space_before = Pt(18)
    p_sub_title.paragraph_format.space_after = Pt(2)
    r_st = p_sub_title.add_run("SUMMER INTERNSHIP PROGRAM SUBMISSION")
    r_st.font.name = "Times New Roman"
    r_st.font.size = Pt(14)
    r_st.bold = True
    r_st.font.color.rgb = COLOR_BLACK

    p_off = doc.add_paragraph()
    p_off.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_off.paragraph_format.space_before = Pt(0)
    p_off.paragraph_format.space_after = Pt(16)
    r_of = p_off.add_run("(FOR OFFICE USE ONLY)")
    r_of.font.name = "Times New Roman"
    r_of.font.size = Pt(11)
    r_of.bold = True
    r_of.font.color.rgb = COLOR_BLACK

    add_body_p(
        doc,
        "Received one copies of Hard Spiral Book and Softcopy of the Summer Internship "
        "Project Report and two copies of Synopsis –",
        space_after=10
    )
    add_body_p(
        doc,
        "Mr. / Ms. Himanshu Pathak Roll No. UAI05BT12417 Specialization: B-Tech AI/ML Contact No.: 9820767182 in partial "
        "fulfilment of requirement for the completion B. Tech as prescribed by the University Grant "
        "Commission (UGC).",
        space_after=10
    )
    add_body_p(
        doc,
        "Project Titled: Full-Stack AI & Clinical Assessment Systems: Engineering the UAi PsychePortal Integrated Suite and ProductivAI Analytics Engine\n"
        "Name of the Organisation: AI Cell, Universal AI University\n"
        "Contact No.: 9820767182\n"
        "Duration: From 4th May 2026 to 14th July 2026\n"
        "Name of Faculty Supervisor: Prof. Rajesh Bhise\n\n"
        "Place: Karjat, Raigad\n"
        "Date:\n\n"
        "Receiver's Signature: ________________\n"
        "Receivers Name: _____________________",
        space_after=0
    )

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 6 (Numbered 7): CONTENTS
    # -----------------------------------------------------------------------
    print("Writing Page 6 (Numbered 7): Contents...")
    p_c_title = doc.add_paragraph()
    p_c_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c_title.paragraph_format.space_before = Pt(18)
    p_c_title.paragraph_format.space_after = Pt(16)
    r_ct = p_c_title.add_run("CONTENTS")
    r_ct.font.name = "Times New Roman"
    r_ct.font.size = Pt(14)
    r_ct.bold = True
    r_ct.font.color.rgb = COLOR_BLACK

    toc_items = [
        ("1. INTRODUCTION", "11", True),
        ("1.1 Overview", "11", False),
        ("1.2 Roles & Responsibility", "12", False),
        ("1.3 Organization Information", "13", False),
        ("2. ANALYSIS OF EXISTING SOLUTION", "13", True),
        ("3. PROPOSED SYSTEM", "15", True),
        ("3.1 Problem Statement", "15", False),
        ("3.2 Methodology Adopted", "16", False),
        ("3.3 Design & Architecture", "17", False),
        ("3.4 Skill Development", "19", False),
        ("4. RESULT & DISCUSSION", "20", True),
        ("4.1 Implementation Details", "20", False),
        ("4.2 Testing Strategies", "23", False),
        ("4.3 Result Analysis", "25", False),
        ("5. CONCLUSION", "27", True),
        ("5.1 Learnings", "27", False),
        ("5.2 Outcomes", "28", False),
        ("5.3 Future Scope", "28", False),
        ("5.4 Final Conclusion", "28", False),
        ("BIBLIOGRAPHY", "29", True),
        ("SYNOPSIS", "30", True),
        ("COMPLETION LETTER", "31", True),
        ("SUMMER INTERNSHIP WEEKLY REPORTS (Weeks 1 to 8)", "32", True)
    ]

    for title, pg, is_bold in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = 1.15
        
        dots_count = max(4, 80 - len(title) - len(pg))
        dots = "." * dots_count
        
        r_t = p.add_run(title + " " + dots + " " + pg)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(11)
        r_t.bold = is_bold
        r_t.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 7 (Numbered 8): List of Figures/ Illustrations
    # -----------------------------------------------------------------------
    print("Writing Page 7 (Numbered 8): List of Figures...")
    p_lf = doc.add_paragraph()
    p_lf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lf.paragraph_format.space_before = Pt(18)
    p_lf.paragraph_format.space_after = Pt(16)
    r_lf = p_lf.add_run("List of Figures/ Illustrations")
    r_lf.font.name = "Times New Roman"
    r_lf.font.size = Pt(14)
    r_lf.bold = True
    r_lf.font.color.rgb = COLOR_BLACK

    tbl_f = doc.add_table(rows=5, cols=3)
    tbl_f.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_f, color="000000", sz="4")
    tbl_f.rows[0].cells[0].width = Inches(1.8)
    tbl_f.rows[0].cells[1].width = Inches(3.8)
    tbl_f.rows[0].cells[2].width = Inches(1.0)
    for row in tbl_f.rows[1:]:
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(3.8)
        row.cells[2].width = Inches(1.0)

    format_cell(tbl_f.rows[0].cells[0], "Figures/\nIllustrations No", bold=True, font_name="Times New Roman", font_size=12)
    format_cell(tbl_f.rows[0].cells[1], "Title / Heading", bold=True, font_name="Times New Roman", font_size=12)
    format_cell(tbl_f.rows[0].cells[2], "Page No.", bold=True, font_name="Times New Roman", font_size=12, align=WD_ALIGN_PARAGRAPH.CENTER)

    f_data = [
        ("1.1", "Development Methodology Flow", "15"),
        ("1.2", "Entity-Relationship Diagram", "17"),
        ("1.3", "Clinical Scoring & Risk State Machine", "18"),
        ("1.4", "Testing Strategy Pyramid", "22")
    ]
    for idx, (c0, c1, c2) in enumerate(f_data):
        row = tbl_f.rows[idx + 1]
        format_cell(row.cells[0], c0, font_name="Times New Roman", font_size=11)
        format_cell(row.cells[1], c1, font_name="Times New Roman", font_size=11)
        format_cell(row.cells[2], c2, font_name="Times New Roman", font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 8 (Numbered 9): List of Tables
    # -----------------------------------------------------------------------
    print("Writing Page 8 (Numbered 9): List of Tables...")
    p_lt = doc.add_paragraph()
    p_lt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lt.paragraph_format.space_before = Pt(18)
    p_lt.paragraph_format.space_after = Pt(16)
    r_lt = p_lt.add_run("List of Tables")
    r_lt.font.name = "Times New Roman"
    r_lt.font.size = Pt(14)
    r_lt.bold = True
    r_lt.font.color.rgb = COLOR_BLACK

    tbl_t = doc.add_table(rows=4, cols=3)
    tbl_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t, color="000000", sz="4")
    tbl_t.rows[0].cells[0].width = Inches(1.8)
    tbl_t.rows[0].cells[1].width = Inches(3.8)
    tbl_t.rows[0].cells[2].width = Inches(1.0)
    for row in tbl_t.rows[1:]:
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(3.8)
        row.cells[2].width = Inches(1.0)

    format_cell(tbl_t.rows[0].cells[0], "Table No", bold=True, font_name="Times New Roman", font_size=12)
    format_cell(tbl_t.rows[0].cells[1], "Table Title / Heading", bold=True, font_name="Times New Roman", font_size=12)
    format_cell(tbl_t.rows[0].cells[2], "Page No.", bold=True, font_name="Times New Roman", font_size=12, align=WD_ALIGN_PARAGRAPH.CENTER)

    t_data = [
        ("1.1", "Organization Information", "12"),
        ("1.2", "Limitations", "14"),
        ("1.3", "Performance Metrics", "24")
    ]
    for idx, (c0, c1, c2) in enumerate(t_data):
        row = tbl_t.rows[idx + 1]
        format_cell(row.cells[0], c0, font_name="Times New Roman", font_size=11)
        format_cell(row.cells[1], c1, font_name="Times New Roman", font_size=11)
        format_cell(row.cells[2], c2, font_name="Times New Roman", font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 9 (Numbered 10): List of Charts
    # -----------------------------------------------------------------------
    print("Writing Page 9 (Numbered 10): List of Charts...")
    p_lc = doc.add_paragraph()
    p_lc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lc.paragraph_format.space_before = Pt(18)
    p_lc.paragraph_format.space_after = Pt(16)
    r_lc = p_lc.add_run("List of Charts")
    r_lc.font.name = "Times New Roman"
    r_lc.font.size = Pt(14)
    r_lc.bold = True
    r_lc.font.color.rgb = COLOR_BLACK

    tbl_c = doc.add_table(rows=4, cols=3)
    tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_c, color="000000", sz="4")
    tbl_c.rows[0].cells[0].width = Inches(1.8)
    tbl_c.rows[0].cells[1].width = Inches(3.8)
    tbl_c.rows[0].cells[2].width = Inches(1.0)
    for row in tbl_c.rows[1:]:
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(3.8)
        row.cells[2].width = Inches(1.0)

    format_cell(tbl_c.rows[0].cells[0], "Chart No", bold=True, font_name="Times New Roman", font_size=12)
    format_cell(tbl_c.rows[0].cells[1], "Chart Title / Heading", bold=True, font_name="Times New Roman", font_size=12)
    format_cell(tbl_c.rows[0].cells[2], "Page No.", bold=True, font_name="Times New Roman", font_size=12, align=WD_ALIGN_PARAGRAPH.CENTER)

    c_data = [
        ("1", "NA", "NA"),
        ("2", "NA", "NA"),
        ("3", "NA", "NA")
    ]
    for idx, (c0, c1, c2) in enumerate(c_data):
        row = tbl_c.rows[idx + 1]
        format_cell(row.cells[0], c0, font_name="Times New Roman", font_size=11)
        format_cell(row.cells[1], c1, font_name="Times New Roman", font_size=11)
        format_cell(row.cells[2], c2, font_name="Times New Roman", font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 10 (Numbered 11): 1. INTRODUCTION (1.1 Overview)
    # -----------------------------------------------------------------------
    print("Writing Page 10 (Numbered 11): Chapter 1 Introduction...")
    add_heading_1(doc, "1. INTRODUCTION")
    add_heading_2(doc, "1.1 Overview")
    add_body_p(
        doc,
        "UAi PsychePortal and ProductivAI represent an integrated full-stack software suite designed to solve "
        "critical challenges in institutional psychological assessment and student productivity analytics. "
        "Higher education environments frequently face hurdles in identifying student mental health distress in "
        "a timely manner and lack actionable tools that quantitatively correlate daily lifestyle routines with "
        "academic performance."
    )
    add_body_p(
        doc,
        "The primary objective of the UAi PsychePortal platform is to eliminate screening turnaround delays "
        "and manual scoring errors by establishing instant digital intake, validated psychometric scoring algorithms, "
        "automated emergency risk triggers, and programmatic PDF diagnostic report generation. The platform features a "
        "dual-tier architecture: the Student Survey Web Portal provides a frictionless, zero-login intake channel on port 5001, "
        "while the Counsellor Single Page Application (SPA) on port 5000 delivers real-time cohort monitoring, risk queues, "
        "and longitudinal trend visualizations for institutional psychologists."
    )
    add_body_p(
        doc,
        "Concurrently, the ProductivAI analytics engine processes lifestyle indicators (including sleep quality, "
        "study hours, physical activity, screen time, and mood ratings) using Scikit-Learn regression pipelines served "
        "through FastAPI on port 8000. By delivering predictive productivity scores and rule-based optimization guidance, "
        "the suite empowers students with empirical self-management insights while providing campus mental health staff "
        "with real-time clinical triage intelligence."
    )
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 11 (Numbered 12): 1.2 Roles & Responsibility
    # -----------------------------------------------------------------------
    print("Writing Page 11 (Numbered 12): Roles & Responsibility...")
    add_heading_2(doc, "1.2 Roles & Responsibility")
    add_body_p(
        doc,
        "As a Summer Intern at the AI Cell, Universal AI University, working under the guidance of my faculty and "
        "institutional mentors, I was engaged as a Full-Stack AI & Clinical Assessment Systems Intern. My responsibilities "
        "spanned both the backend and frontend layers of the product, in addition to core system design, machine learning "
        "modeling, testing, and technical documentation activities."
    )
    add_heading_3(doc, "Backend & Database Development")
    add_bullet_item(doc, "", "Assisted in designing the relational database schema, including the User, StudentProfile, Assessment, SubscaleScore, RiskAlert, and ProductivityLog entities and their foreign key constraints.")
    add_bullet_item(doc, "", "Developed API route handlers for psychometric intake, scoring calculations, ReportLab PDF generation, and Excel exports.")
    add_bullet_item(doc, "", "Implemented the atomic assessment pipeline, ensuring survey responses, subscale totals, and emergency risk flags are committed transactionally.")
    add_bullet_item(doc, "", "Built the automated emergency alert logic that triggers instant counsellor notifications when a student score reaches Moderate, Severe, or Extremely Severe categories.")
    add_heading_3(doc, "Frontend & Machine Learning Engineering")
    add_bullet_item(doc, "", "Built the responsive React SPA dashboard using Vite, TailwindCSS, and Chart.js for real-time risk heatmaps and student cohort views.")
    add_bullet_item(doc, "", "Developed the FastAPI machine learning service, training and serializing Random Forest regression models to predict lifestyle productivity scores.")
    add_bullet_item(doc, "", "Created multi-process PowerShell and Batch scripts (launch_all.bat) for automated single-click deployment across all microservices.")
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 12 (Numbered 13): 1.3 Organization Information & 2. ANALYSIS OF EXISTING SOLUTION
    # -----------------------------------------------------------------------
    print("Writing Page 12 (Numbered 13): Organization Info & Chapter 2...")
    add_heading_2(doc, "1.3 Organization Information")
    
    tbl_org = doc.add_table(rows=6, cols=2)
    tbl_org.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_org, color="000000", sz="4")
    tbl_org.rows[0].cells[0].width = Inches(2.2)
    tbl_org.rows[0].cells[1].width = Inches(4.3)
    for row in tbl_org.rows[1:]:
        row.cells[0].width = Inches(2.2)
        row.cells[1].width = Inches(4.3)

    org_fields = [
        ("Field", "Details"),
        ("Name", "Prof. Rajesh Bhise / Dr. Shivaji Pawar"),
        ("Designation", "Faculty Mentor / Head of Department"),
        ("Contact Number", "+91 2192 664000"),
        ("Email ID", "aicell@universalai.in"),
        ("Company Website", "Universal AI University: https://www.universalai.in")
    ]
    for idx, (f0, f1) in enumerate(org_fields):
        row = tbl_org.rows[idx]
        format_cell(row.cells[0], f0, bold=(idx==0), font_name="Calibri", font_size=11)
        format_cell(row.cells[1], f1, bold=(idx==0), font_name="Calibri", font_size=11)

    p_cap_org = doc.add_paragraph()
    p_cap_org.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_org.paragraph_format.space_before = Pt(4)
    p_cap_org.paragraph_format.space_after = Pt(10)
    r_co = p_cap_org.add_run("Table 1.1 – Organization Information")
    r_co.font.name = "Calibri"
    r_co.font.size = Pt(11)

    add_heading_1(doc, "2. ANALYSIS OF EXISTING SOLUTION")
    add_body_p(
        doc,
        "Traditional psychological screening and wellness monitoring workflows in educational institutions rely on "
        "paper-based questionnaires or isolated spreadsheets (Google Sheets / Microsoft Excel). This creates delays, "
        "inconsistency, and diagnostic risk that the UAi PsychePortal suite is engineered to eliminate."
    )
    add_heading_3(doc, "Survey of Commonly Used Existing Approaches")
    add_body_p(
        doc,
        "Before UAi PsychePortal was proposed, institutions typically relied on one or a combination of the following "
        "approaches to manage student evaluations:"
    )
    add_bullet_item(doc, "Spreadsheet-Based Tracking (Google Sheets / Microsoft Excel): ", "The most common approach. Counsellors manually record raw Likert answers. However, formula maintenance, complex reverse scoring (6 - R), and role permissions must be custom-built, which most clinical staff lack the technical training to maintain safely.")
    add_bullet_item(doc, "Generic Survey Tools (Google Forms / Microsoft Forms): ", "Used for gathering intake data, but lack automatic linkage between student submissions and clinical subscale scoring, offer no emergency risk state machines, and cannot compile formal diagnostic PDF records.")
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 13 (Numbered 14): 2. ANALYSIS (Survey contd & Gap Analysis)
    # -----------------------------------------------------------------------
    print("Writing Page 13 (Numbered 14): Survey Contd & Gap Analysis...")
    add_bullet_item(doc, "Manual Paper Questionnaires: ", "Physical test sheets distributed in classrooms. Tests must be collected, manually summed, and physically archived, imposing a 3 to 14 day delay before counsellors can review results and identify students requiring immediate support.")
    add_bullet_item(doc, "Third-Party Automation Stitching: ", "Attempting to stitch together web forms with webhook triggers. While this improves intake speed, these setups are fragile to API changes, lack centralized authentication, and offer no role-based data isolation for sensitive psychological records.")

    add_heading_2(doc, "Gap Analysis")
    add_body_p(
        doc,
        "Across all of the above approaches, three recurring structural gaps were identified:"
    )
    add_bullet_item(doc, "1. No Atomicity Between Survey Intake and Scoring / Alert Creation: ", "In manual and spreadsheet workflows, capturing student responses and evaluating clinical cutoffs are disconnected steps. If a student submits an assessment indicating acute severe distress, no automated alert is generated until a counsellor manually opens and recalculates the spreadsheet days later.")
    add_bullet_item(doc, "2. No Automatic Triage & Stopping Logic: ", "None of the existing tools automatically transition student records through clinical triage stages. Flagged students remain unmonitored without automated case assignment or structured intervention logging.")
    add_bullet_item(doc, "3. No Role-Based Isolation with Clinical Confidentiality: ", "General-purpose tools either give all staff unrestricted access to sensitive student mental health data or make sharing so restrictive that multidisciplinary teams cannot collaborate securely.")
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 14 (Numbered 15): Limitations Table (Table 1.2)
    # -----------------------------------------------------------------------
    print("Writing Page 14 (Numbered 15): Limitations Table...")
    add_body_p(
        doc,
        "single, atomic, system-guaranteed workflow – removing the human dependency at each of these handoff points."
    )
    add_heading_2(doc, "Limitations of Existing Solutions")

    tbl_lim = doc.add_table(rows=5, cols=3)
    tbl_lim.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_lim, color="000000", sz="4")
    tbl_lim.rows[0].cells[0].width = Inches(1.8)
    tbl_lim.rows[0].cells[1].width = Inches(2.4)
    tbl_lim.rows[0].cells[2].width = Inches(2.4)
    for row in tbl_lim.rows[1:]:
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(2.4)
        row.cells[2].width = Inches(2.4)

    format_cell(tbl_lim.rows[0].cells[0], "Feature Area", bold=True, font_name="Times New Roman", font_size=11)
    format_cell(tbl_lim.rows[0].cells[1], "Legacy / Manual Solution", bold=True, font_name="Times New Roman", font_size=11)
    format_cell(tbl_lim.rows[0].cells[2], "UAi PsychePortal Solution", bold=True, font_name="Times New Roman", font_size=11)

    lim_rows = [
        ("Screening Response Time", "Manual paper scoring with an average delay of 3–14 days, causing crisis intervention delays.", "Near-instant processing with automated scoring in 12ms and instant counsellor alert generation."),
        ("Scoring Reliability", "Manual grading and spreadsheet reverse-coding (6 - R), highly prone to mathematical error.", "Automated standardized scoring engine with 100% verified computational accuracy across all norms."),
        ("Risk Flagging Logic", "Manual review of score sheets, prone to missing severe depression or anxiety indicators.", "Automatic stopping and escalation rules flag Moderate and Severe distress the moment survey is submitted."),
        ("Clinical Confidentiality & Access", "Single shared sheet with high risk of unauthorized exposure of sensitive student data.", "Role-based access control isolating administrative counsellor endpoints from unauthorized access.")
    ]
    for idx, (c0, c1, c2) in enumerate(lim_rows):
        row = tbl_lim.rows[idx + 1]
        format_cell(row.cells[0], c0, bold=True, font_name="Times New Roman", font_size=10)
        format_cell(row.cells[1], c1, bold=False, font_name="Times New Roman", font_size=10)
        format_cell(row.cells[2], c2, bold=False, font_name="Times New Roman", font_size=10)

    p_cap_lim = doc.add_paragraph()
    p_cap_lim.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_lim.paragraph_format.space_before = Pt(4)
    p_cap_lim.paragraph_format.space_after = Pt(8)
    r_cl = p_cap_lim.add_run("Table 1.2 – Limitations")
    r_cl.font.name = "Calibri"
    r_cl.font.size = Pt(11)

    add_heading_1(doc, "3. PROPOSED SYSTEM", space_before=10, space_after=3)
    add_heading_2(doc, "3.1 Problem Statement", space_before=6, space_after=3)
    add_body_p(doc, "Educational institutions face three primary challenges in student psychological screening:", space_after=3)
    add_bullet_item(doc, "Screening Friction: ", "The delay between a student's intake submission and counsellor scoring directly hampers early crisis intervention.", space_after=2)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 15 (Numbered 16): 3. PROPOSED SYSTEM (Methodology & Figure 1.1)
    # -----------------------------------------------------------------------
    print("Writing Page 15 (Numbered 16): Proposed System & Figure 1.1...")
    add_bullet_item(doc, "Follow-up Inconsistency: ", "Students flagged with subclinical distress frequently lack timely automated tracking, allowing symptom escalation before institutional intervention.", space_after=2)
    add_bullet_item(doc, "Operational Overhead: ", "Counsellors spend hours manually grading questionnaires and drafting reports rather than engaging directly in clinical consultation.", space_after=3)
    add_body_p(
        doc,
        "UAi PsychePortal solves this by establishing a unified clinical assessment engine that automates intake, "
        "computes validated scores, flags crisis risks instantly, and compiles comprehensive diagnostic PDF reports on demand.",
        space_after=4
    )

    add_heading_2(doc, "3.2 Methodology Adopted", space_before=6, space_after=3)
    add_body_p(
        doc,
        "The development of UAi PsychePortal followed an Agile, API-First, and Component-Driven Software Development Lifecycle, "
        "moving from data modeling through to a fully interactive dashboard in four coordinated stages.",
        space_after=3
    )

    add_figure(doc, FIG1_1, "Figure 1.1 – Development Methodology Flow", width_inches=5.2)

    add_bullet_item(doc, "Domain & Data-First Modeling: ", "The database schema was designed first, to enforce constraints, relationships, and assessment scoring rules at the database level.", space_after=2)
    add_bullet_item(doc, "API-First Architecture: ", "Core backend services and mathematical scoring engines were built and tested before connecting frontend user interfaces.", space_after=2)
    add_bullet_item(doc, "State Machine Design: ", "Risk escalation transitions were implemented as atomic, all-or-nothing operations so that alert states and notifications remain synchronized.", space_after=2)
    add_bullet_item(doc, "Asynchronous Background Operations: ", "Non-blocking side effects — sending counsellor email alerts, logging audit trails, and generating diagnostic PDFs — were offloaded cleanly.", space_after=2)
    add_bullet_item(doc, "Modern UI & Design System: ", "An accessible, responsive dashboard was built using React SPA with Vite, Chart.js visualizations, and TailwindCSS.", space_after=2)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 16 (Numbered 17): 3.3 Design & Architecture (Tech Stack Overview)
    # -----------------------------------------------------------------------
    print("Writing Page 16 (Numbered 17): Design & Architecture...")
    add_heading_2(doc, "3.3 Design & Architecture")
    add_heading_3(doc, "Technology Stack Overview")
    add_bullet_item(doc, "Framework: ", "A modern full-stack web framework (Flask 3.0) with server-rendered routes and REST API blueprints.")
    add_bullet_item(doc, "Language: ", "Python 3.13 layered across the backend, scoring engine, ReportLab PDF builder, and machine learning models.")
    add_bullet_item(doc, "Database & ORM: ", "SQLAlchemy ORM managing SQLite for development/offline modes and PostgreSQL for cloud deployment.")
    add_bullet_item(doc, "Authentication & Security: ", "Flask-Login session management paired with Bcrypt salted password hashing and CSRF token protection.")
    add_bullet_item(doc, "Styling & UI: ", "React 18 Single Page Application styled with TailwindCSS utility classes, Lucide icons, and Chart.js.")
    add_bullet_item(doc, "Reporting & Export: ", "Programmatic ReportLab engine for compiling multi-page diagnostic PDF dossiers, plus Pandas/OpenPyXL for Excel exports.")
    add_bullet_item(doc, "Machine Learning Engine: ", "FastAPI asynchronous service running Scikit-Learn regression pipelines serialized via Joblib.")
    add_bullet_item(doc, "Deployment & Automation: ", "Multi-process PowerShell and Batch orchestrators executing single-click deployment across all services.")

    add_heading_3(doc, "Entity-Relationship Design")
    add_body_p(
        doc,
        "The relational database schema models six core entities: User, StudentProfile, Assessment, SubscaleScore, "
        "RiskAlert, and ProductivityLog. Referential integrity is strictly enforced via foreign keys, cascading deletions, "
        "and indexed lookups."
    )
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 17 (Numbered 18): Figure 1.2 ER Diagram & Lead State Machine Text
    # -----------------------------------------------------------------------
    print("Writing Page 17 (Numbered 18): Figure 1.2 ER Diagram...")
    add_figure(doc, FIG1_2, "Figure 1.2 – Entity-Relationship Diagram", width_inches=6.0)

    add_heading_3(doc, "Clinical Scoring State Machine & Stopping Rules")
    add_body_p(
        doc,
        "When an assessment is submitted, it enters a defined lifecycle. It begins as Submitted, moves into Scoring "
        "where item responses are validated and reverse-coded (6 - R), and then progresses to Threshold Evaluation. "
        "Subscale totals are checked against clinical cutoffs. The moment any subscale evaluates to Moderate or Severe, "
        "an Emergency Risk Alert is triggered, immediately pushing notifications to the Counsellor Dashboard. "
        "If scores remain within normal ranges, the record transitions to Archived Normal status followed by PDF compilation."
    )
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 18 (Numbered 19): Figure 1.3 State Machine & 3.4 Skill Development (Part 1)
    # -----------------------------------------------------------------------
    print("Writing Page 18 (Numbered 19): Figure 1.3 & Skill Development Part 1...")
    add_figure(doc, FIG1_3, "Figure 1.3 – Clinical Scoring & Risk State Machine", width_inches=5.8)

    add_body_p(
        doc,
        "The stopping condition is evaluated for every assessment: clinical triage remains active until all subscale scores "
        "are computed. The moment Moderate or Severe distress is detected, an emergency alert state is locked into the database, "
        "and priority counsellor notifications are dispatched."
    )

    add_heading_2(doc, "3.4 Skill Development")
    add_body_p(
        doc,
        "Through the technical design and execution of UAi PsychePortal and ProductivAI, the following engineering "
        "capabilities were acquired and strengthened:"
    )
    add_bullet_item(doc, "Full-Stack Framework Mastery: ", "Building modern Flask application factories, modular blueprints, dynamic Jinja2 script injection, and high-performance React SPAs with Vite.")
    add_bullet_item(doc, "Relational Database Architecture & Schema Design: ", "Structuring normalized relational schemas with foreign-key constraints, cascading rules, and atomic multi-table transactions.")
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 19 (Numbered 20): 3.4 Skill Development (Part 2) & 4. RESULT & DISCUSSION (Subsystems 1 & 2)
    # -----------------------------------------------------------------------
    print("Writing Page 19 (Numbered 20): Skill Development Part 2 & Chapter 4...")
    add_bullet_item(doc, "Enterprise Authentication & Security: ", "Integrating Bcrypt password cryptography, secure session cookies, and strict role-based route access controls.")
    add_bullet_item(doc, "Machine Learning Lifecycle Engineering: ", "Synthesizing 50,000 lifestyle records, training Random Forest regression estimators, serializing models via Joblib, and serving predictions via FastAPI REST endpoints.")
    add_bullet_item(doc, "Data Visualization & Programmatic Document Generation: ", "Developing responsive Chart.js analytics dashboards and compiling multi-page clinical PDF dossiers using ReportLab flowables.")

    add_heading_1(doc, "4. RESULT & DISCUSSION")
    add_heading_2(doc, "4.1 Implementation Details")
    add_heading_3(doc, "1. Authentication & Session Management")
    add_body_p(
        doc,
        "When an administrator or counsellor accesses the platform, the authentication middleware verifies credentials "
        "against salted Bcrypt password hashes stored in the User table. Active sessions are maintained through cryptographically "
        "signed HTTP-only cookies, with role decorators preventing unauthorized access to counsellor dashboards."
    )
    add_heading_3(doc, "2. Relational Database Modeling & SQLAlchemy ORM")
    add_body_p(
        doc,
        "The schema defines entities for User, StudentProfile, Assessment, SubscaleScore, RiskAlert, and ProductivityLog. "
        "Database transactions guarantee that assessment submissions, subscale scores, and alert flags are committed atomically, "
        "preventing partial or corrupted clinical records."
    )
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 20 (Numbered 21): 4.1 Subsystems 3 to 6
    # -----------------------------------------------------------------------
    print("Writing Page 20 (Numbered 21): Subsystems 3 to 6...")
    add_heading_3(doc, "3. Standardized Psychometric Scoring Engines (app/scoring.py)")
    add_body_p(
        doc,
        "The scoring module implements mathematical formulas for validated clinical instruments: Lovibond DASS-21 "
        "(summing 7 items per dimension with a x2 multiplier to match DASS-42 norms), Big Five Inventory BFI-44 "
        "(incorporating 16 reverse-coded items using the 6 - R transformation), and Empathy / Systemizing Quotients (EQ/SQ)."
    )
    add_heading_3(doc, "4. Automated Crisis Risk Flagging & Alert Dispatch")
    add_body_p(
        doc,
        "The scoring pipeline evaluates computed subscales against established clinical thresholds. If a student's DASS-21 "
        "Depression score exceeds 14, Anxiety exceeds 10, or Stress exceeds 19, an emergency RiskAlert record is generated. "
        "The Counsellor Dashboard immediately highlights the student profile card with a pulsing crimson badge."
    )
    add_heading_3(doc, "5. Programmatic Dynamic PDF Generation Engine (ReportLab)")
    add_body_p(
        doc,
        "Utilizing ReportLab's SimpleDocTemplate and TableStyle flowables, the system dynamically compiles multi-page clinical "
        "diagnostic dossiers featuring student demographics, subscale breakdown tables, normative classification charts, "
        "and personalized therapeutic recommendations within 850 milliseconds of request."
    )
    add_heading_3(doc, "6. Standalone Student Survey Web Portal (Port 5001)")
    add_body_p(
        doc,
        "A dedicated Flask microservice running on port 5001 provides a frictionless, zero-login intake portal. Students select "
        "their cohort, navigate paginated question cards with smooth transitions, and submit responses directly to the shared "
        "relational database."
    )
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 21 (Numbered 22): 4.1 Subsystems 7 to 11
    # -----------------------------------------------------------------------
    print("Writing Page 21 (Numbered 22): Subsystems 7 to 11...")
    add_heading_3(doc, "7. Transactional Email Notification Engine")
    add_body_p(
        doc,
        "An automated notification service dispatches priority alerts to campus counsellors the moment a student evaluates "
        "to Moderate or Severe distress, including student details, subscale scores, and contact information to expedite triage."
    )
    add_heading_3(doc, "8. Interactive Counsellor SPA Dashboard (Port 5000 / React 18)")
    add_body_p(
        doc,
        "The administrative frontend is an enterprise-grade Single Page Application built with React 18, Vite, and TailwindCSS. "
        "It features 11 dedicated views including Risk Alert Center, Longitudinal Trends, Student Directory, and Assessment Deployer, "
        "utilizing Chart.js for real-time radar and bar analytics."
    )
    add_heading_3(doc, "9. ProductivAI Machine Learning Engine (FastAPI / Port 8000)")
    add_body_p(
        doc,
        "ProductivAI processes a synthesized 50,000-sample dataset modeling lifestyle indicators (sleep quality, study hours, "
        "screen time, exercise, and mood). A Random Forest Regressor (R² = 0.912) is served via FastAPI to return predicted "
        "productivity scores (0-100) and feature importance breakdowns in under 15ms."
    )
    add_heading_3(doc, "10. ProductivAI Interactive Frontend")
    add_body_p(
        doc,
        "Features interactive score dials, habit adjustment sliders, and rule-based behavioral guidance cards, allowing students "
        "to simulate how altering specific habits directly improves predicted productivity."
    )
    add_heading_3(doc, "11. Offline Psychometric Assessment GUI (Tkinter)")
    add_body_p(
        doc,
        "A native desktop application built with Python Tkinter enables offline questionnaire administration in campus computer "
        "labs without internet connectivity, batch-syncing responses upon network availability."
    )
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 22 (Numbered 23): 4.1 Subsystem 12 & 4.2 Testing Strategies (Figure 1.4)
    # -----------------------------------------------------------------------
    print("Writing Page 22 (Numbered 23): Subsystem 12 & Testing Pyramid...")
    add_heading_3(doc, "12. Deployment & Scheduled Job Infrastructure")
    add_body_p(
        doc,
        "Automated Windows Batch and PowerShell orchestrators (launch_all.bat / .ps1) initialize virtual environments, execute "
        "database migrations, verify port bindings (5000, 5001, 8000), and launch all services simultaneously with zero configuration."
    )

    add_heading_2(doc, "4.2 Testing Strategies")
    add_body_p(
        doc,
        "To ensure software quality, clinical precision, and system resilience, a multi-tiered testing hierarchy was executed, "
        "moving from fast unit tests at the base up to full system validation at the top."
    )

    add_figure(doc, FIG1_4, "Figure 1.4 – Testing Strategy Pyramid", width_inches=5.8)

    add_heading_3(doc, "Unit & Schema Validation Testing")
    add_bullet_item(doc, "", "Validated database model constraints, foreign key cascades, and payload parsers.")
    add_bullet_item(doc, "", "Verified mathematical scoring formulations and reverse-keying transformations (6 - R) against reference psychometric tables.")
    add_bullet_item(doc, "", "Confirmed safe default imputations for missing survey items without application crashes.")
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 23 (Numbered 24): 4.2 Testing Details (Unit, API, Security, State Machine)
    # -----------------------------------------------------------------------
    print("Writing Page 23 (Numbered 24): Testing Details...")
    add_heading_3(doc, "API & Integration Testing")
    add_bullet_item(doc, "Public Intake Test: ", "Verified that the public intake endpoint on port 5001 returns HTTP 201 for valid payloads and HTTP 400 for malformed submissions.")
    add_bullet_item(doc, "ML Prediction Endpoint Test: ", "Verified that POST /predict on port 8000 validates input ranges (sleep hours 0-14, study hours 0-16) and returns valid score predictions in under 15ms.")
    add_bullet_item(doc, "PDF Generation Pipeline Test: ", "Confirmed that ReportLab generates valid, uncorrupted multi-page PDF binaries for arbitrary student profiles.")

    add_heading_3(doc, "Security & Access Control Testing")
    add_bullet_item(doc, "Route Protection: ", "Verified that middleware correctly redirects unauthenticated requests away from counsellor routes to the login page.")
    add_bullet_item(doc, "Password Security: ", "Confirmed that Bcrypt hashing introduces adequate work factor latency (~80ms) to thwart brute-force attacks.")

    add_heading_3(doc, "State Machine & Concurrency Testing")
    add_bullet_item(doc, "Emergency Risk State Transition: ", "Simulated assessment submissions with high depression scores and verified that RiskAlert records are created atomically and rendered immediately on the dashboard.")
    add_bullet_item(doc, "Concurrent Ingestion Integrity: ", "Verified that multiple simultaneous submissions in SQLite WAL mode maintain zero data corruption or race conditions.")
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 24 (Numbered 25): 4.3 Result Analysis & Table 1.3 Performance Metrics & Summary
    # -----------------------------------------------------------------------
    print("Writing Page 24 (Numbered 25): Result Analysis & Table 1.3...")
    add_heading_2(doc, "4.3 Result Analysis")
    add_body_p(
        doc,
        "The implementation of UAi PsychePortal and ProductivAI produced measurable improvements in system performance, "
        "data integrity, and clinical workflow efficiency."
    )
    add_heading_3(doc, "Performance Metrics & Key Benchmarks")

    tbl_perf = doc.add_table(rows=6, cols=4)
    tbl_perf.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_perf, color="000000", sz="4")
    tbl_perf.rows[0].cells[0].width = Inches(1.8)
    tbl_perf.rows[0].cells[1].width = Inches(1.5)
    tbl_perf.rows[0].cells[2].width = Inches(1.6)
    tbl_perf.rows[0].cells[3].width = Inches(1.4)
    for row in tbl_perf.rows[1:]:
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(1.5)
        row.cells[2].width = Inches(1.6)
        row.cells[3].width = Inches(1.4)

    perf_h = ["Metric", "Target Benchmark", "Measured Result", "Status"]
    for idx, h in enumerate(perf_h):
        format_cell(tbl_perf.rows[0].cells[idx], h, bold=True, font_name="Times New Roman", font_size=10)

    perf_rows = [
        ("API Intake Latency", "Under 200 MS", "72 MS – 110 MS", "Passed"),
        ("Database Transaction Time", "Under 50 MS", "18 MS", "Passed"),
        ("Clinical Scoring Execution", "Under 50 MS", "12 MS", "Passed"),
        ("ReportLab PDF Render", "Under 2,000 MS", "850 MS", "Passed"),
        ("ML Inference Latency", "Under 50 MS", "14 MS", "Passed")
    ]
    for idx, (c0, c1, c2, c3) in enumerate(perf_rows):
        row = tbl_perf.rows[idx + 1]
        format_cell(row.cells[0], c0, bold=True, font_name="Times New Roman", font_size=9.5)
        format_cell(row.cells[1], c1, bold=False, font_name="Times New Roman", font_size=9.5)
        format_cell(row.cells[2], c2, bold=False, font_name="Times New Roman", font_size=9.5)
        format_cell(row.cells[3], c3, bold=True, font_name="Times New Roman", font_size=9.5)

    p_cap_perf = doc.add_paragraph()
    p_cap_perf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_perf.paragraph_format.space_before = Pt(4)
    p_cap_perf.paragraph_format.space_after = Pt(10)
    r_cp = p_cap_perf.add_run("Table 1.3 – Performance Metrics")
    r_cp.font.name = "Times New Roman"
    r_cp.font.size = Pt(11)

    add_heading_3(doc, "Summary of Key Outcomes")
    add_bullet_item(doc, "Zero Crisis Window Latency: ", "Automated risk flagging identifies severe depression and anxiety cases within milliseconds of survey completion, completely eliminating the 3 to 14 day delay typical of paper workflows.")
    add_bullet_item(doc, "Eliminated Manual Scoring Errors: ", "Standardized mathematical logic guarantees 100% computational fidelity across reverse-scored psychometric inventories.")
    add_bullet_item(doc, "Automated Diagnostic Dossiers: ", "Dynamic ReportLab compilation generates comprehensive multi-page diagnostic PDFs instantly, saving counsellors 35–45 minutes per student.")
    add_bullet_item(doc, "Actionable Predictive Analytics: ", "FastAPI machine learning pipelines provide students with quantified lifestyle impact breakdowns and personalized optimization strategies.")
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 25 (Numbered 26): 4.3 Qualitative Observations & Scalability Observations
    # -----------------------------------------------------------------------
    print("Writing Page 25 (Numbered 26): Qualitative Observations...")
    add_heading_2(doc, "Qualitative Observations")
    add_body_p(
        doc,
        "Beyond the raw performance numbers, the shift from a manual, spreadsheet-driven workflow to an automated, "
        "state-driven pipeline produced several qualitative improvements that were consistently observed during testing "
        "and internal walkthroughs:"
    )
    add_bullet_item(doc, "Reduced Cognitive Load on Staff: ", "Because scoring, severity evaluation, and risk alerting are now system-enforced rather than memory-dependent, counsellors no longer need to manually grade questionnaires or calculate reverse scores, freeing up time for direct clinical consultation.")
    add_bullet_item(doc, "Consistent Diagnostic Experience: ", "Every assessment – regardless of testing channel or cohort – receives identical standardized scoring and normative classification, removing human grading variance.")
    add_bullet_item(doc, "Faster Emergency Response: ", "Instant dashboard alerts on severe distress mean counsellors are typically aware of critical student cases within seconds, compared to the multi-day delays common in manual workflows.")

    add_heading_3(doc, "Scalability Observations")
    add_body_p(
        doc,
        "Load testing during development (simulating concurrent assessment submissions across multiple student cohorts) "
        "showed that the atomic transaction design held up correctly under concurrent writes – zero cases of an assessment "
        "being recorded without its corresponding subscales or risk flags, and zero data leakage across user profiles. "
        "This validates the core design decision to enforce transactional consistency and schema constraints at the database "
        "layer rather than relying solely on application-level checks."
    )
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 26 (Numbered 27): Limitations Identified & 5. CONCLUSION (5.1 Learnings)
    # -----------------------------------------------------------------------
    print("Writing Page 26 (Numbered 27): Limitations & Chapter 5 Learnings...")
    add_heading_2(doc, "Limitations Identified")
    add_body_p(
        doc,
        "A few limitations were also noted during result analysis, which could inform future iterations of the platform:"
    )
    add_bullet_item(doc, "", "The offline Tkinter desktop client requires manual network re-connection to synchronize locally stored batch files with the primary SQLite database.")
    add_bullet_item(doc, "", "Machine learning models currently operate on a fixed trained checkpoint; implementing automated periodic retraining with incoming longitudinal student feedback will further refine predictive accuracy.")
    add_bullet_item(doc, "", "Notification dispatch currently relies on local SMTP protocols rather than a dedicated cloud transactional email API provider (such as Resend or SendGrid).")

    add_heading_1(doc, "5. CONCLUSION")
    add_heading_2(doc, "5.1 Learnings")
    add_bullet_item(doc, "Full-Stack Development in Practice: ", "Gained hands-on experience in connecting backend logic (database design, APIs) with frontend implementation on a real production system.")
    add_bullet_item(doc, "Transaction-Safe System Design: ", "Learned why critical clinical operations, such as assessment scoring and risk alerting, must be handled atomically to avoid inconsistent records.")
    add_bullet_item(doc, "Multi-Service Architecture: ", "Understood how to coordinate multiple decoupled microservices (Flask, React, FastAPI) sharing a common relational database.")
    add_bullet_item(doc, "Role-Based Access Control: ", "Learned to design and enforce permission boundaries across student and counsellor roles using centralized middleware.")
    add_bullet_item(doc, "Structured Testing: ", "Applied a layered testing approach – unit, integration, and security testing – to validate the system systematically.")
    add_bullet_item(doc, "Professional Documentation: ", "Improved my ability to document and communicate a technical system clearly, as required in an industry setting.")
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 27 (Numbered 28): 5.2 Outcomes, 5.3 Future Scope, 5.4 Final Conclusion
    # -----------------------------------------------------------------------
    print("Writing Page 27 (Numbered 28): Outcomes, Future Scope, Conclusion...")
    add_heading_2(doc, "5.2 Outcomes")
    add_bullet_item(doc, "", "Contributed to the design and development of UAi PsychePortal and ProductivAI, a working multi-service clinical assessment and productivity platform.")
    add_bullet_item(doc, "", "Implemented an automated intake-to-scoring pipeline, removing the manual grading delays identified in Section 2.")
    add_bullet_item(doc, "", "Built and validated role-based access control across Admin, Counsellor, and Student roles.")
    add_bullet_item(doc, "", "Delivered a tested system meeting key performance benchmarks (detailed in Section 4.3).")
    add_bullet_item(doc, "", "Produced complete technical documentation, including architecture diagrams and testing results.")

    add_heading_2(doc, "5.3 Future Scope")
    add_bullet_item(doc, "Configurable Scoring Protocols: ", "Allow counsellors to define custom assessment rubrics and modify subscale threshold boundaries dynamically.")
    add_bullet_item(doc, "Cloud Containerization: ", "Package the Flask, React, and FastAPI microservices into Docker containers for scalable Kubernetes deployment.")
    add_bullet_item(doc, "Cross-Platform Mobile Application: ", "Extend student survey intake to native mobile applications built with Flutter or React Native.")
    add_bullet_item(doc, "Generative Clinical Summaries: ", "Integrate secure local LLMs to draft preliminary clinical consultation summaries from longitudinal assessment histories.")

    add_heading_2(doc, "5.4 Final Conclusion")
    add_body_p(
        doc,
        "This Summer Internship Program at the AI Cell, Universal AI University gave me the opportunity to apply "
        "academic knowledge to a real, industry-grade software project. Working on UAi PsychePortal and ProductivAI involved "
        "practical exposure to secure system design, clinical scoring formulations, machine learning deployment, testing, and "
        "technical documentation, under the guidance of my faculty and institutional mentors. The internship strengthened my "
        "technical foundation and gave me a clearer understanding of professional software development practices."
    )
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 28 (Numbered 29): BIBLIOGRAPHY
    # -----------------------------------------------------------------------
    print("Writing Page 28 (Numbered 29): Bibliography...")
    add_heading_1(doc, "BIBLIOGRAPHY")
    references = [
        "1. Pallets Projects. (2026). Flask Documentation. Retrieved from https://flask.palletsprojects.com/",
        "2. SQLAlchemy Authors. (2026). SQLAlchemy ORM Documentation. Retrieved from https://www.sqlalchemy.org/",
        "3. Tiangolo, S. (2026). FastAPI Documentation. Retrieved from https://fastapi.tiangolo.com/",
        "4. Meta Open Source. (2026). React Documentation. Retrieved from https://react.dev/",
        "5. Vite Core Team. (2026). Vite Build Tooling Documentation. Retrieved from https://vitejs.dev/",
        "6. Tailwind Labs Inc. (2026). Tailwind CSS Documentation. Retrieved from https://tailwindcss.com/docs",
        "7. Scikit-Learn Developers. (2026). Scikit-Learn Machine Learning Documentation. Retrieved from https://scikit-learn.org/",
        "8. ReportLab Europe Ltd. (2026). ReportLab PDF Generation User Guide. Retrieved from https://www.reportlab.com/docs/",
        "9. Lovibond, S.H. & Lovibond, P.F. (1995). Manual for the Depression Anxiety Stress Scales (DASS-21). Psychology Foundation.",
        "10. John, O.P. & Srivastava, S. (1999). The Big Five Trait Taxonomy (BFI-44). Handbook of Personality."
    ]
    for r_text in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        run_ref = p_ref.add_run(r_text)
        run_ref.font.name = "Times New Roman"
        run_ref.font.size = Pt(11)
        run_ref.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 29 (Numbered 30): SYNOPSIS
    # -----------------------------------------------------------------------
    print("Writing Page 29 (Numbered 30): Synopsis...")
    add_heading_1(doc, "SYNOPSIS")
    add_heading_3(doc, "Title")
    add_body_p(doc, "Full-Stack AI & Clinical Assessment Systems: Engineering the UAi PsychePortal Integrated Suite and ProductivAI Analytics Engine", space_after=6)

    add_heading_3(doc, "Problem")
    add_body_p(
        doc,
        "Higher education institutions face increasing challenges in monitoring student psychological wellness and productivity. "
        "Traditional approaches – paper screening forms, spreadsheets, or disconnected desktop tools – lack automatic scoring, "
        "suffer from severe delays (3–14 days) in alerting counsellors to acute distress, and offer no empirical tools to correlate "
        "daily habits (sleep, study, screen time) with academic cognitive output.",
        space_after=6
    )

    add_heading_3(doc, "Solution")
    add_body_p(
        doc,
        "UAi PsychePortal is an integrated full-stack software suite that automates the psychological screening and triage lifecycle. "
        "It ingests assessments instantly through a standalone web portal (port 5001), evaluates standardized clinical scores "
        "(DASS-21, BFI-44 with 6-R reverse scoring, EQ, SQ), and triggers real-time emergency flags for Moderate and Severe distress "
        "on the Counsellor SPA (port 5000). Dynamic ReportLab builders compile multi-page diagnostic PDFs on demand, while the "
        "ProductivAI engine (FastAPI on port 8000) predicts productivity outcomes using Scikit-Learn regression models trained on "
        "50,000 lifestyle records.",
        space_after=6
    )

    add_heading_3(doc, "Key Features")
    add_bullet_item(doc, "", "Multi-Service Architecture: Decoupled Flask core (5000), Survey portal (5001), React SPA, and FastAPI ML service (8000).")
    add_bullet_item(doc, "", "Standardized Clinical Scoring: Zero-defect implementations of Lovibond DASS-21, BFI-44, and Baron-Cohen EQ/SQ.")
    add_bullet_item(doc, "", "Automated Crisis Risk Triage: Real-time event triggers for severe distress with instant dashboard highlighting.")
    add_bullet_item(doc, "", "Predictive ML Analytics: Random Forest Regressor predicting productivity scores with relative feature weights.")

    add_heading_3(doc, "Results")
    add_body_p(
        doc,
        "Reduced clinical screening turnaround time from 7+ days to under 100 milliseconds, achieved 100% scoring precision, "
        "saved campus counsellors 35–45 minutes per student evaluation via automated ReportLab PDF dossiers, and provided students "
        "with an empirical tool to optimize lifestyle routines and academic wellness.",
        space_after=0
    )
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 30 (Numbered 31): COMPLETION LETTER
    # -----------------------------------------------------------------------
    print("Writing Page 30 (Numbered 31): Completion Letter...")
    p_cl = doc.add_paragraph()
    p_cl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cl.paragraph_format.space_before = Pt(10)
    p_cl.paragraph_format.space_after = Pt(10)
    r_cl = p_cl.add_run("COMPLETION LETTER")
    r_cl.font.name = "Times New Roman"
    r_cl.font.size = Pt(14)
    r_cl.bold = True
    r_cl.font.color.rgb = COLOR_BLACK

    if os.path.exists(OFFER_LETTER_IMG):
        p_cimg = doc.add_paragraph()
        p_cimg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cimg.paragraph_format.space_before = Pt(0)
        p_cimg.paragraph_format.space_after = Pt(0)
        r_ci = p_cimg.add_run()
        r_ci.add_picture(OFFER_LETTER_IMG, width=Inches(5.4))

    # -----------------------------------------------------------------------
    # SECTION 2: SUMMER INTERNSHIP WEEKLY REPORTS (PAGES 31 TO 43)
    # -----------------------------------------------------------------------
    print("Configuring Section 2: Weekly Reports (Pages 31 to 43)...")
    sec2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec2.top_margin = Inches(0.8)
    sec2.bottom_margin = Inches(0.8)
    sec2.left_margin = Inches(0.9)
    sec2.right_margin = Inches(0.9)
    sec2.page_width = Inches(8.27)
    sec2.page_height = Inches(11.69)
    sec2.header.is_linked_to_previous = False
    sec2.footer.is_linked_to_previous = False

    # Data for all 8 weeks
    tasks_w1 = [
        ("Requirement analysis, architectural design, and repository layout setup for UAi PsychePortal.", "Completed"),
        ("Defined SQLAlchemy database schema (User, StudentProfile, Assessment, SubscaleScore).", "Completed"),
        ("Implemented Flask application factory pattern and dynamic configuration handling.", "Completed"),
        ("Configured environment variables and established development SQLite database.", "Completed")
    ]
    tools_w1 = [
        "Python 3.13, Flask 3.0.0",
        "Flask-SQLAlchemy, SQLite",
        "Git, VS Code"
    ]
    outcomes_w1 = [
        "Standardized database normalization techniques for relational models storing psychometric profiles.",
        "Configured Flask application factory patterns to isolate development and production environments.",
        "Improved understanding of schema migrations and relational constraints in SQLAlchemy."
    ]
    challenges_w1 = [
        "Cyclic imports between models, database initializers, and authentication blueprints.",
        "SQLite foreign key support requiring explicit PRAGMA foreign_keys = ON activation."
    ]
    solutions_w1 = [
        "Implemented Application Factory pattern (create_app) in app/__init__.py, decoupling declarations.",
        "Configured SQLite connection listeners in SQLAlchemy to automatically enforce foreign key constraints."
    ]
    plans_w1 = [
        ("Implement DASS-21, BFI-44, EQ, and SQ mathematical scoring functions", "2 days"),
        ("Create automated risk-flagging logic for Moderate/Severe student scores", "3 days"),
        ("Develop seed data scripts (seed_questions.py, seed_demo_data.py)", "2 days")
    ]

    tasks_w2 = [
        ("Implemented scoring algorithms for DASS-21, BFI-44, EQ, and SQ in app/scoring.py", "Completed"),
        ("Engineered automated emergency risk flagging for Moderate/Severe subscale categories", "Completed"),
        ("Created database population scripts for 100+ demo profiles and question banks", "Completed")
    ]
    tools_w2 = [
        "Python 3.13, SQLAlchemy ORM, SQLite",
        "Flask-Bcrypt, Flask-Login",
        "PyTest unit testing framework"
    ]
    outcomes_w2 = [
        "Mastered reverse-score transformations (6 - R) and subscale matrix indexing for Big Five inventory metrics.",
        "Developed automated event triggers in SQLAlchemy to flag high-risk entries upon submission.",
        "Strengthened understanding of psychometric norm cutoffs across psychological evaluation standards."
    ]
    challenges_w2 = [
        "Handling missing item selections without crashing subscale calculations.",
        "Ensuring atomic rollback if subscale score insertion fails midway during assessment intake."
    ]
    solutions_w2 = [
        "Defaulted missing responses to neutral values (3 for BFI-44, 0 for DASS-21) inside safe map retrievals.",
        "Wrapped entire intake and scoring evaluation inside SQLAlchemy transaction context managers."
    ]
    plans_w2 = [
        ("Construct programmatic PDF report builder using ReportLab", "2 days"),
        ("Implement Excel data export using Pandas and OpenPyXL", "2 days"),
        ("Build Student Survey Web Portal on port 5001", "1 day")
    ]

    tasks_w3 = [
        ("Developed PDF export generation using ReportLab (SimpleDocTemplate, TableStyle)", "Completed"),
        ("Built Excel export features for counsellor metrics using Pandas and OpenPyXL", "Completed"),
        ("Deployed standalone Flask Student Survey Portal running on port 5001", "Completed")
    ]
    tools_w3 = [
        "ReportLab 4.1.0, Pandas 2.1.4, OpenPyXL 3.1.2",
        "Flask Jinja2 Templating, SQLite WAL Mode",
        "Postman API Testing"
    ]
    outcomes_w3 = [
        "Standardized programmatic document formatting using ReportLab flowables, tables, and page breaks.",
        "Integrated dual-Flask microservice instances sharing a common SQLite relational database.",
        "Gained practical knowledge of dynamic canvas styling and custom header/footer drawing in ReportLab."
    ]
    challenges_w3 = [
        "PDF layout text overflow when rendering student assessment details across page boundaries.",
        "Concurrent SQLite database lock contention between student survey intake and counsellor queries."
    ]
    solutions_w3 = [
        "Encapsulated tabular cell text within Paragraph flowables with automated auto-wrapping text styles.",
        "Enabled SQLite Write-Ahead Logging (WAL) mode and tuned timeout configurations to 30 seconds."
    ]
    plans_w3 = [
        ("Develop modern React SPA Counsellor Dashboard using Vite and TailwindCSS", "2 days"),
        ("Build 11 dashboard view modules (Risk Alerts, Directory, Deployer)", "3 days"),
        ("Configure interactive Chart.js visualizations for subscale trend analysis", "2 days")
    ]

    tasks_w4 = [
        ("Built Vite + React single-page application inside uai-counsellor-dashboard/", "Completed"),
        ("Designed 11 dynamic views featuring TailwindCSS styling and Lucide icons", "Completed"),
        ("Configured interactive Chart.js visualizations for subscale trend analysis", "Completed")
    ]
    tools_w4 = [
        "React 18, Vite 5, TailwindCSS 3.4",
        "Chart.js 4.4, Lucide-React",
        "REST API integration"
    ]
    outcomes_w4 = [
        "Engineered dynamic dashboard views using React state hooks (useState, useEffect, useMemo).",
        "Applied responsive design patterns using TailwindCSS utilities and CSS custom variables.",
        "Built reusable modal dialogs, data tables with search filters, and risk indicator badges."
    ]
    challenges_w4 = [
        "Integrating client-side React routes into Flask server-rendered endpoints without 404 errors.",
        "Chart.js canvas memory leaks upon repeated view switching in single-page navigation."
    ]
    solutions_w4 = [
        "Compiled Vite static assets into Flask's static directory and rendered root <div> via Jinja2 catch-all.",
        "Implemented clean destroy lifecycle hooks in Chart.js React wrapper components."
    ]
    plans_w4 = [
        ("Connect React frontend with Flask database using Jinja2 JSON script injection", "2 days"),
        ("Develop ProductivAI synthetic dataset generator (50,000 samples)", "2 days"),
        ("Train and serialize Random Forest ML productivity regression model", "3 days")
    ]

    tasks_w5 = [
        ("Connected React frontend with Flask database using Jinja2 JSON script injection", "Completed"),
        ("Built 50,000-sample synthetic lifestyle dataset generator (generate_dataset.py)", "Completed"),
        ("Trained Random Forest Regressor and exported model via Joblib (productivity_model.pkl)", "Completed")
    ]
    tools_w5 = [
        "Scikit-Learn 1.3, Joblib, NumPy, Pandas",
        "FastAPI, Uvicorn, Python 3.13",
        "Git, PowerShell"
    ]
    outcomes_w5 = [
        "Evaluated regression models using metrics such as R², MAE, and MSE.",
        "Deserialized trained .pkl estimators inside FastAPI endpoints for real-time inference.",
        "Understood synthetic data generation distributions matching empirical psychological research norms."
    ]
    challenges_w5 = [
        "Model inference latency spikes when serving REST requests under heavy batch scoring loads.",
        "Feature scaling inconsistencies between Scikit-Learn training pipelines and runtime inputs."
    ]
    solutions_w5 = [
        "Cached the deserialized Joblib model instance in global application memory upon FastAPI startup.",
        "Bundled Scikit-Learn Pipeline object containing both the StandardScaler and Random Forest Regressor."
    ]
    plans_w5 = [
        ("Develop ProductivAI React analytics dashboard with score dials and Recharts", "2 days"),
        ("Create unified multi-process orchestrators (launch_all.bat and launch_all.ps1)", "2 days"),
        ("Execute full system integration verification across ports 5000, 5001, and 8000", "1 day")
    ]

    tasks_w6 = [
        ("Built ProductivAI React analytics dashboard with score dials and dark/light themes", "Completed"),
        ("Created unified multi-process orchestrators (launch_all.bat and launch_all.ps1)", "Completed"),
        ("Executed full system integration verification across ports 5000, 5001, and 8000", "Completed")
    ]
    tools_w6 = [
        "Windows Batch Scripting, PowerShell 7",
        "React 18, Recharts 2.10, Framer Motion",
        "FastAPI, Uvicorn, Flask"
    ]
    outcomes_w6 = [
        "Automated multi-process application deployment using shell scripting techniques.",
        "Verified cross-origin data flows and API request validation across distinct microservices.",
        "Mastered real-time visualization of multi-dimensional feature importances in Recharts."
    ]
    challenges_w6 = [
        "Managing multiple terminal windows and port collisions during full-stack startup.",
        "Browser CORS blocking cross-origin requests between port 5000 and port 8000."
    ]
    solutions_w6 = [
        "Wrote automated PowerShell start routines with explicit port bindings (-port 5000, -port 5001, -port 8000).",
        "Enabled FastAPI CORSMiddleware with granular allowed origins allow_origins=['http://localhost:5000']."
    ]
    plans_w6 = [
        ("Conduct end-to-end integration testing across Flask, React, and FastAPI backends", "2 days"),
        ("Validate offline Tkinter desktop assessment sync workflows with SQLite persistence", "2 days"),
        ("Optimize database query indexes for subscale score aggregations and risk queues", "1 day")
    ]

    tasks_w7 = [
        ("Conducted end-to-end integration testing across Flask, React, and FastAPI backends", "Completed"),
        ("Validated offline Tkinter desktop assessment sync workflows with SQLite persistence", "Completed"),
        ("Optimized database query indexes for subscale score aggregations and risk queues", "Completed")
    ]
    tools_w7 = [
        "Python 3.13, PyTest, SQLite WAL Mode",
        "Tkinter Desktop GUI, Postman API Testing",
        "SQLite EXPLAIN QUERY PLAN"
    ]
    outcomes_w7 = [
        "Mastered integration testing patterns for microservices sharing common persistence layers.",
        "Gained proficiency in SQLite query profiling and compound index optimization.",
        "Designed robust offline sync reconciliation algorithms for educational campus computer labs."
    ]
    challenges_w7 = [
        "Synchronizing offline desktop assessment logs with relational server database without duplicates.",
        "Subscale query latency increasing as test submission volume scaled above 1,000 records."
    ]
    solutions_w7 = [
        "Implemented deterministic timestamp UUID matching to resolve batch data insertion conflicts.",
        "Created compound B-Tree indexes on (student_id, assessment_type, created_at) across assessment tables."
    ]
    plans_w7 = [
        ("Generate optimized production builds for React SPA and static assets", "2 days"),
        ("Conduct user acceptance testing and live demonstrations with campus counsellors", "2 days"),
        ("Finalize technical project handbook, architectural blueprints, and user guides", "3 days")
    ]

    tasks_w8 = [
        ("Generated optimized production builds for React SPA (npm run build) and static assets", "Completed"),
        ("Conducted user acceptance testing and live demonstrations with campus counsellors", "Completed"),
        ("Verified core functionalities including clinical scoring, emergency triage, and PDF generation", "Completed"),
        ("Finalized technical project handbook, architectural blueprints, and user guides", "Completed")
    ]
    tools_w8 = [
        "Vite, TailwindCSS, PowerShell, ReportLab",
        "Microsoft Word, Docx2Pdf, GitHub",
        "PyTest, Chrome DevTools"
    ]
    outcomes_w8 = [
        "Understood software deployment lifecycle and production release procedures.",
        "Learned rigorous technical documentation practices for institutional deliverables.",
        "Improved debugging and cross-platform verification skills.",
        "Gained experience in delivering production-ready full-stack software applications."
    ]
    challenges_w8 = [
        "Final cross-browser responsive layout validation on high-DPI displays.",
        "Ensuring feature stability during multi-service launch orchestration across varied machines.",
        "Preparing complete academic deliverable matching university guidelines."
    ]
    solutions_w8 = [
        "Conducted comprehensive end-to-end integration and smoke tests across browsers.",
        "Refactored launcher automation scripts with graceful error recovery and path detection.",
        "Verified all documentation sections against official university reference standards."
    ]

    # -----------------------------------------------------------------------
    # PAGE 31: Week 1 Header, Student & Company Tables, Week 1 Tasks
    # -----------------------------------------------------------------------
    print("Writing Page 31: Week 1 Header & Tasks...")
    add_weekly_header(doc)
    p_wrt = doc.add_paragraph()
    p_wrt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_wrt.paragraph_format.space_before = Pt(2)
    p_wrt.paragraph_format.space_after = Pt(4)
    r_wrt = p_wrt.add_run("Summer Internship Weekly Report")
    r_wrt.font.name = "Times New Roman"
    r_wrt.font.size = Pt(16)
    r_wrt.bold = True
    r_wrt.font.color.rgb = COLOR_BLACK

    add_student_company_tables(doc)
    add_weekly_meta(doc, "1st Week", "04 May 2026 - 10 May 2026")
    add_task_table(doc, tasks_w1)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 32: Week 1 Tools, Outcomes, Challenges & Solutions
    # -----------------------------------------------------------------------
    print("Writing Page 32: Week 1 Tools & Outcomes...")
    add_weekly_header(doc)
    add_tech_tools(doc, tools_w1)
    add_learning_outcomes(doc, outcomes_w1)
    add_challenges_solutions(doc, challenges_w1, solutions_w1)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 33: Week 1 Plan, Week 2 Meta, Tasks, Tools, Outcomes
    # -----------------------------------------------------------------------
    print("Writing Page 33: Week 1 Next Plan & Week 2...")
    add_weekly_header(doc)
    add_plan_table(doc, plans_w1)
    add_weekly_meta(doc, "2nd Week", "11 May 2026 - 17 May 2026")
    add_task_table(doc, tasks_w2)
    add_tech_tools(doc, tools_w2)
    add_learning_outcomes(doc, outcomes_w2)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 34: Week 2 Challenges, Week 2 Plan, Week 3 Meta, Tasks, Tools
    # -----------------------------------------------------------------------
    print("Writing Page 34: Week 2 Challenges & Week 3...")
    add_weekly_header(doc)
    add_challenges_solutions(doc, challenges_w2, solutions_w2)
    add_plan_table(doc, plans_w2)
    add_weekly_meta(doc, "3rd week", "18 May 2026 - 24 May 2026")
    add_task_table(doc, tasks_w3)
    add_tech_tools(doc, tools_w3)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 35: Week 3 Outcomes, Challenges, Week 3 Plan, Week 4 Meta, Tasks
    # -----------------------------------------------------------------------
    print("Writing Page 35: Week 3 Outcomes & Week 4 Tasks...")
    add_weekly_header(doc)
    add_learning_outcomes(doc, outcomes_w3)
    add_challenges_solutions(doc, challenges_w3, solutions_w3)
    add_plan_table(doc, plans_w3)
    add_weekly_meta(doc, "4th week", "25 May 2026 - 31 May 2026")
    add_task_table(doc, tasks_w4)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 36: Week 4 Tools, Outcomes, Challenges, Week 4 Plan
    # -----------------------------------------------------------------------
    print("Writing Page 36: Week 4 Tools, Outcomes & Plan...")
    add_weekly_header(doc)
    add_tech_tools(doc, tools_w4)
    add_learning_outcomes(doc, outcomes_w4)
    add_challenges_solutions(doc, challenges_w4, solutions_w4)
    add_plan_table(doc, plans_w4)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 37: Midterm Digital Signature
    # -----------------------------------------------------------------------
    print("Writing Page 37: Midterm Signature...")
    add_weekly_header(doc)
    p_sig_mid = doc.add_paragraph()
    p_sig_mid.paragraph_format.space_before = Pt(36)
    p_sig_mid.paragraph_format.space_after = Pt(12)
    r_sm = p_sig_mid.add_run("Student Signature: (Digital Signature)")
    r_sm.font.name = "Times New Roman"
    r_sm.font.size = Pt(11)
    r_sm.bold = True
    r_sm.font.color.rgb = COLOR_BLACK

    if os.path.exists(STUDENT_SIGNATURE_IMG):
        p_sig_img = doc.add_paragraph()
        p_sig_img.paragraph_format.left_indent = Inches(0.8)
        p_sig_img.paragraph_format.space_after = Pt(0)
        r_img = p_sig_img.add_run()
        r_img.add_picture(STUDENT_SIGNATURE_IMG, width=Inches(1.8))

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 38: Week 5 Header, Student & Company Tables, Week 5 Tasks, Tools
    # -----------------------------------------------------------------------
    print("Writing Page 38: Week 5 Header, Tables & Tasks...")
    add_weekly_header(doc)
    p_wrt5 = doc.add_paragraph()
    p_wrt5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_wrt5.paragraph_format.space_before = Pt(2)
    p_wrt5.paragraph_format.space_after = Pt(4)
    r_wrt5 = p_wrt5.add_run("Summer Internship Weekly Report")
    r_wrt5.font.name = "Times New Roman"
    r_wrt5.font.size = Pt(16)
    r_wrt5.bold = True
    r_wrt5.font.color.rgb = COLOR_BLACK

    add_student_company_tables(doc)
    add_weekly_meta(doc, "5th week", "01 June 2026 - 07 June 2026")
    add_task_table(doc, tasks_w5)
    add_tech_tools(doc, tools_w5)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 39: Week 5 Outcomes, Challenges, Week 5 Plan
    # -----------------------------------------------------------------------
    print("Writing Page 39: Week 5 Outcomes & Plan...")
    add_weekly_header(doc)
    add_learning_outcomes(doc, outcomes_w5)
    add_challenges_solutions(doc, challenges_w5, solutions_w5)
    add_plan_table(doc, plans_w5)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 40: Week 6 Meta, Tasks, Tools, Outcomes, Challenges
    # -----------------------------------------------------------------------
    print("Writing Page 40: Week 6 Meta, Tasks, Outcomes & Challenges...")
    add_weekly_header(doc)
    add_weekly_meta(doc, "6th week", "08 June 2026 - 14 June 2026")
    add_task_table(doc, tasks_w6)
    add_tech_tools(doc, tools_w6)
    add_learning_outcomes(doc, outcomes_w6)
    add_challenges_solutions(doc, challenges_w6, solutions_w6)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 41: Week 6 Plan, Week 7 Meta, Tasks, Tools, Outcomes, Challenges
    # -----------------------------------------------------------------------
    print("Writing Page 41: Week 6 Plan & Week 7 Meta, Tasks, Challenges...")
    add_weekly_header(doc)
    add_plan_table(doc, plans_w6)
    add_weekly_meta(doc, "7th week", "15 June 2026 - 21 June 2026")
    add_task_table(doc, tasks_w7)
    add_tech_tools(doc, tools_w7)
    add_learning_outcomes(doc, outcomes_w7)
    add_challenges_solutions(doc, challenges_w7, solutions_w7)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 42: Week 7 Plan, Week 8 Meta, Tasks, Tools
    # -----------------------------------------------------------------------
    print("Writing Page 42: Week 7 Plan & Week 8 Tasks...")
    add_weekly_header(doc)
    add_plan_table(doc, plans_w7)
    add_weekly_meta(doc, "8th week", "22 June 2026 - 14 July 2026")
    add_task_table(doc, tasks_w8)
    add_tech_tools(doc, tools_w8)
    doc.add_page_break()

    # -----------------------------------------------------------------------
    # PAGE 43: Week 8 Outcomes, Challenges, Final Signatures
    # -----------------------------------------------------------------------
    print("Writing Page 43: Week 8 Outcomes & Final Signature...")
    add_weekly_header(doc)
    add_learning_outcomes(doc, outcomes_w8)
    add_challenges_solutions(doc, challenges_w8, solutions_w8)

    p_sig_final = doc.add_paragraph()
    p_sig_final.paragraph_format.space_before = Pt(18)
    p_sig_final.paragraph_format.space_after = Pt(10)
    r_sf = p_sig_final.add_run("Student Signature: (Digital Signature)")
    r_sf.font.name = "Times New Roman"
    r_sf.font.size = Pt(11)
    r_sf.bold = True
    r_sf.font.color.rgb = COLOR_BLACK

    if os.path.exists(STUDENT_SIGNATURE_IMG):
        p_sig_img = doc.add_paragraph()
        p_sig_img.paragraph_format.left_indent = Inches(0.8)
        p_sig_img.paragraph_format.space_after = Pt(0)
        r_img = p_sig_img.add_run()
        r_img.add_picture(STUDENT_SIGNATURE_IMG, width=Inches(1.8))

    # Save document
    print(f"Saving Word document to {OUTPUT_DOCX}...")
    doc.save(OUTPUT_DOCX)
    print("DOCX successfully generated.")

    try:
        shutil.copy2(OUTPUT_DOCX, DOWNLOADS_DOCX)
        print(f"Copied DOCX to {DOWNLOADS_DOCX}")
    except Exception as e:
        print(f"Downloads copy warning: {e}")

    # Convert to PDF
    print(f"Converting DOCX to PDF: {OUTPUT_PDF}...")
    try:
        docx2pdf.convert(OUTPUT_DOCX, OUTPUT_PDF)
        print(f"PDF successfully compiled at {OUTPUT_PDF}")
        try:
            shutil.copy2(OUTPUT_PDF, DOWNLOADS_PDF)
            print(f"Copied PDF to {DOWNLOADS_PDF}")
        except Exception as e:
            print(f"Downloads PDF copy warning: {e}")
    except Exception as e:
        print(f"PDF conversion error: {e}")

    print("=" * 70)
    print("EXACT UNIVERSITY FORMAT SIP HANDBOOK COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    main()
