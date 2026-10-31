import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
import shutil
import os

from weekly_report_builder import (
    TEMPLATE_PATH, WEEKLY_DATA, TECH_STACK_TABLE_DATA,
    set_cell_background, set_cell_margins, set_table_borders,
    format_cell, build_weekly_report_section
)
from report_blocks import (
    LOGO_IMG_PATH, ARCH_IMG_PATH, WORKFLOW_IMG_PATH,
    OUTPUT_DOC_PATH, OUTPUT_DOWNLOADS_PATH,
    add_heading_1, add_heading_2, add_heading_3,
    add_body_p, add_bullet_item, add_code_block, add_formula_box
)

def build_cover_page(doc):
    """Constructs a formal university cover / title page."""
    # Add university logo if exists
    if os.path.exists(LOGO_IMG_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(4)
        run_logo = p_logo.add_run()
        run_logo.add_picture(LOGO_IMG_PATH, width=Inches(3.2))

    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(4)
    p_uni.paragraph_format.space_after = Pt(2)
    r = p_uni.add_run("UNIVERSAL AI UNIVERSITY, KARJAT")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0x0F, 0x2D, 0x59)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(0)
    p_dept.paragraph_format.space_after = Pt(24)
    r = p_dept.add_run("School of Ai & Future Technologies\nEstablished vide Maharashtra Act No. III of 2023 | Recognized by UGC Act 1956")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

    # Document Category
    p_cat = doc.add_paragraph()
    p_cat.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cat.paragraph_format.space_before = Pt(10)
    p_cat.paragraph_format.space_after = Pt(12)
    r = p_cat.add_run("— SUMMER INTERNSHIP PROJECT REPORT —")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

    # Report Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(10)
    p_title.paragraph_format.line_spacing = 1.25
    r = p_title.add_run("Full-Stack AI & Clinical Assessment Systems:\nEngineering the UAi PsychePortal Integrated Suite and ProductivAI Analytics Engine")
    r.font.name = "Times New Roman"
    r.font.size = Pt(17)
    r.bold = True
    r.font.color.rgb = RGBColor(0x0A, 0x19, 0x2F)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(28)
    r = p_sub.add_run("A Comprehensive Technical Project Report Submitted in Partial Fulfillment of the\nRequirements for the Degree of Bachelor of Technology in Artificial Intelligence & Machine Learning")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.italic = True
    r.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    # Metadata Table
    tbl_meta = doc.add_table(rows=6, cols=2)
    tbl_meta.style = "Table Grid"
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_meta, color="CBD5E1", sz="4")
    
    widths = [Inches(2.8), Inches(3.2)]
    for row in tbl_meta.rows:
        for idx, w in enumerate(widths):
            row.cells[idx].width = w

    metadata_entries = [
        ("Student Name: ", "Himanshu Pathak", "Roll No.: ", "UAI05BT12417"),
        ("Academic Year: ", "2nd Year, 4th Semester", "Email ID: ", "himanshu.pathak@universalai.in"),
        ("Department: ", "School of Ai & Future Tech.", "Host Organization: ", "Ai Cell, Universal Ai University"),
        ("Faculty Mentor: ", "Prof. Rajesh Bhise", "Designation: ", "Vertical Head – Innovation & Project"),
        ("Industry Co-Mentor: ", "Dr. Shivaji Pawar", "Location: ", "Karjat Campus, Maharashtra"),
        ("Submission Date: ", "September 22, 2026", "Status: ", "Final Deliverable Submitted")
    ]

    for r_idx, (k1, v1, k2, v2) in enumerate(metadata_entries):
        format_cell(tbl_meta.rows[r_idx].cells[0], k1, v1, bg_color="F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
        format_cell(tbl_meta.rows[r_idx].cells[1], k2, v2, bg_color="F8FAFC" if r_idx % 2 == 0 else "FFFFFF")

    doc.add_page_break()

def build_executive_summary(doc):
    add_heading_1(doc, "Executive Summary / Abstract")
    
    add_body_p(doc, 
        "This technical project report documents the design, architectural integration, mathematical scoring mechanisms, "
        "machine learning pipelines, and full-stack software development executed during the AI Cell Internship at Universal "
        "Ai University. The work encompasses two major production-grade software ecosystems: (1) UAi PsychePortal, a multi-service "
        "psychological assessment and counsellor management platform designed for educational institutions, and (2) ProductivAI, "
        "an AI-driven personal productivity analyzer that utilizes predictive machine learning to evaluate lifestyle indicators "
        "and output personalized optimization strategies."
    )
    
    add_body_p(doc, 
        "The UAi PsychePortal unifies four distinct technical components: a robust Flask core backend featuring object-relational "
        "mapping (SQLAlchemy), a high-performance single-page application (SPA) built with React 18, Vite, and TailwindCSS for real-time "
        "risk tracking, a standalone student survey web interface, and an offline psychometric desktop application built with Python Tkinter. "
        "The platform implements standardized scoring algorithms for clinical instruments, including DASS-21 (Depression, Anxiety, Stress Scale), "
        "BFI-44 (Big Five Inventory), Emotional Quotient (EQ), and Systemizing Quotient (SQ), while automatically raising emergency risk flags "
        "and compiling multi-page dynamic PDF diagnostic reports using ReportLab."
    )
    
    add_body_p(doc, 
        "Concurrently, the ProductivAI engine processes a 50,000-sample synthetic dataset mapping daily routines (sleep quality, study hours, "
        "exercise, screen time, social media consumption, and mood metrics) to productivity outcomes (0–100 score). Utilizing Scikit-Learn "
        "regression models (Linear Regression and Random Forest Regressor) serialized via Joblib and served through FastAPI REST endpoints, "
        "ProductivAI provides automated factor breakdowns, rule-based AI recommendations, and interactive UI charts."
    )
    
    add_body_p(doc, 
        "The combined codebase demonstrates production deployment techniques, including dynamic Jinja2 asset bootstrapping, cross-origin API "
        "orchestration, database migration management with Flask-Migrate, and multi-process orchestrator automation via PowerShell and Windows Batch."
    )
    
    # Keywords callout box
    add_formula_box(doc, 
        "Full-Stack Engineering, Clinical Psychometrics, Machine Learning, Mental Health Analytics, DASS-21, BFI-44, "
        "FastAPI, Flask, React SPA, TailwindCSS, Random Forest Regressor, Automated Risk Triage, ReportLab PDF, Multi-Process Orchestration.",
        label="Keywords & Index Terms:"
    )
    
    doc.add_page_break()

def build_table_of_contents(doc):
    add_heading_1(doc, "Table of Contents")
    
    toc_items = [
        ("1. Title Page & Institutional Metadata", "1"),
        ("2. Executive Summary / Abstract", "2"),
        ("3. Introduction & Background", "4"),
        ("    3.1 Problem Context", "4"),
        ("    3.2 Domain & Engineering Objectives", "4"),
        ("4. Core Body — Technical Analysis", "5"),
        ("    4.1 System Architecture & Architecture Diagram", "5"),
        ("    4.2 Folder & Module Breakdown", "6"),
        ("    4.3 Methodology & Pipeline Details", "7"),
        ("        4.3.1 Relational Database Schema & Authentication", "7"),
        ("        4.3.2 Clinical Instrument Scoring Formulas & Risk Triage", "8"),
        ("        4.3.3 Machine Learning Pipeline (ProductivAI)", "9"),
        ("    4.4 Technology Stack & Software Ecosystem", "10"),
        ("5. Results & Discussion", "11"),
        ("    5.1 System Accomplishments & Operational Workflow", "11"),
        ("    5.2 Advantages of the Engineered Approach", "12"),
        ("    5.3 Limitations & Technical Constraints", "12"),
        ("    5.4 Future Scope & Architectural Roadmap", "13"),
        ("6. Conclusion", "14"),
        ("7. References", "14"),
        ("PART 2: SUMMER INTERNSHIP WEEKLY PROGRESS REPORTS", "15"),
        ("    Weekly Report — Week 1 (4-May-2026 to 9-May-2026)", "15"),
        ("    Weekly Report — Week 2 (11-May-2026 to 16-May-2026)", "16"),
        ("    Weekly Report — Week 3 (18-May-2026 to 23-May-2026)", "17"),
        ("    Weekly Report — Week 4 (25-May-2026 to 30-May-2026)", "18"),
        ("    Weekly Report — Week 5 (1-Jun-2026 to 6-Jun-2026)", "19"),
        ("    Weekly Report — Week 6 (8-Jun-2026 to 13-Jun-2026)", "20")
    ]
    
    tbl_toc = doc.add_table(rows=len(toc_items), cols=2)
    tbl_toc.style = "Table Grid"
    set_table_borders(tbl_toc, color="E2E8F0", sz="2")
    
    for r_idx, (section_title, page_no) in enumerate(toc_items):
        tbl_toc.rows[r_idx].cells[0].width = Inches(5.2)
        tbl_toc.rows[r_idx].cells[1].width = Inches(0.8)
        
        is_bold = not section_title.startswith("    ")
        bg = "F8FAFC" if is_bold and not section_title.startswith("PART") else ("EFF6FF" if section_title.startswith("PART") else "FFFFFF")
        
        format_cell(tbl_toc.rows[r_idx].cells[0], None, section_title, 
                    font_size=10.5 if is_bold else 10, bg_color=bg)
        if is_bold:
            tbl_toc.rows[r_idx].cells[0].paragraphs[0].runs[0].bold = True
            
        format_cell(tbl_toc.rows[r_idx].cells[1], None, page_no, 
                    font_size=10.5 if is_bold else 10, bg_color=bg, align=WD_ALIGN_PARAGRAPH.RIGHT)
        if is_bold:
            tbl_toc.rows[r_idx].cells[1].paragraphs[0].runs[0].bold = True

    doc.add_page_break()

def build_introduction(doc):
    add_heading_1(doc, "3. Introduction & Background")
    
    add_heading_2(doc, "3.1 Problem Context")
    add_body_p(doc, 
        "Modern educational institutions face increasing challenges in monitoring, evaluating, and supporting student mental health "
        "and academic productivity. Traditional psychological screening methods in academic environments rely on paper-based assessments, "
        "isolated desktop tools, or manual scoring spreadsheets. These legacy workflows suffer from significant operational drawbacks:"
    )
    
    add_bullet_item(doc, "1. Delayed Risk Identification: ", 
        "Manual evaluation of paper assessments creates significant latency between student testing and crisis intervention by university "
        "counsellors, increasing the exposure of vulnerable students during critical distress phases."
    )
    add_bullet_item(doc, "2. Data Fragmentation: ", 
        "Student screening records, risk logs, demographic profiles, and historical assessment timelines remain scattered across "
        "non-interoperable spreadsheets or disconnected desktop applications, preventing holistic longitudinal monitoring."
    )
    add_bullet_item(doc, "3. Lack of Actionable Productivity Insights: ", 
        "Students lack empirical tools to understand how daily routine habits (such as sleep quality, study sessions, exercise frequency, "
        "and screen time) quantitatively correlate with and dictate daily cognitive performance and academic output."
    )
    
    add_heading_2(doc, "3.2 Domain & Engineering Objectives")
    add_body_p(doc, 
        "To systematically address these institutional challenges, the project engineered an end-to-end synchronized software infrastructure "
        "capable of handling clinical data securely, computing validated psychological scores in real time, alerting campus mental health "
        "staff to elevated risk levels, and delivering machine-learning-driven productivity analytics."
    )
    
    add_body_p(doc, "The key engineering objectives achieved during this internship encompass:")
    add_bullet_item(doc, "• Clinical Instrument Automation: ", 
        "Implementing exact mathematical formulas, reverse-item transformations, and multi-tier threshold evaluation for DASS-21, BFI-44, EQ, and SQ tests."
    )
    add_bullet_item(doc, "• Microservice & Full-Stack Integration: ", 
        "Coupling a Flask micro-backend serving SQLite/PostgreSQL with a React SPA counsellor interface by injecting dynamic JSON script payloads "
        "(window.__FLASK_KPIS__, window.__FLASK_FLAGGED_STUDENTS__) into server-rendered Jinja2 bootstrap templates."
    )
    add_bullet_item(doc, "• Predictive Machine Learning: ", 
        "Training and serializing regressor models on lifestyle features to predict productivity indices with sub-millisecond API response latency using FastAPI and Scikit-Learn."
    )
    add_bullet_item(doc, "• Automated Diagnostic Reporting: ", 
        "Dynamically building multi-page institutional PDF reports containing formatted demographic tables, visual subscale severity bars, and confidentiality notices using ReportLab graphics pipelines."
    )

def build_system_architecture(doc):
    add_heading_1(doc, "4. Core Body — Technical Analysis")
    
    add_heading_2(doc, "4.1 System Architecture")
    add_body_p(doc, 
        "The overall repository is engineered into two primary decoupled operational ecosystems: (1) The UAi PsychePortal Ecosystem, "
        "which coordinates psychological testing, scoring, database management, and counsellor risk triage; and (2) The ProductivAI ML System, "
        "which provides machine-learning lifestyle analytics and productivity predictions. The interaction between these subsystems is illustrated below:"
    )
    
    # Embed Architecture Image
    if os.path.exists(ARCH_IMG_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(ARCH_IMG_PATH, width=Inches(5.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run("Figure 1: High-Level System Architecture and Inter-Service Orchestration Diagram.")
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    add_heading_2(doc, "4.2 Folder & Module Breakdown")
    add_body_p(doc, "The repository structure enforces separation of concerns across service layers:")
    
    add_bullet_item(doc, "• Root Application Entry (run.py, config.py): ", 
        "Initializes the primary Flask application instance, configures environment-specific database URIs, sets CSRF parameters, "
        "and exposes database management scripts."
    )
    add_bullet_item(doc, "• Core Flask Application Package (app/): ", 
        "Encapsulates application blueprints (auth, student, counsellor, admin, faculty), SQLAlchemy data models (app/models.py), "
        "clinical scoring engines (app/scoring.py), and PDF/Excel generation engines (app/reports.py)."
    )
    add_bullet_item(doc, "• Counsellor Dashboard SPA (uai-counsellor-dashboard/): ", 
        "A responsive React 18 single-page application bundled with Vite and TailwindCSS, featuring 11 active views including "
        "the Student Directory, Real-Time Risk Alerts, Assessment Deployer, Interventions Logger, and Executive Analytics."
    )
    add_bullet_item(doc, "• Student Survey Web Portal (student-survey-portal/): ", 
        "A lightweight Flask portal hosted on port 5001 enabling rapid, distraction-free assessment taking for registered students."
    )
    add_bullet_item(doc, "• Psychometric Desktop Client (UAI_Quiz_App/): ", 
        "A native Python Tkinter GUI desktop client enabling offline clinical assessments using standalone JSON question pools."
    )
    add_bullet_item(doc, "• ProductivAI Engine (ProductivAI/): ", 
        "Houses the FastAPI backend (main.py), synthetic dataset generation pipeline (generate_dataset.py), Scikit-Learn training suite "
        "(model_training.py), and dedicated React frontend."
    )
    add_bullet_item(doc, "• Integrated Launcher Suite (integrated_launcher/): ", 
        "Provides automated multi-process orchestration via launch_all.ps1 and launch_all.bat to concurrently spawn backend and frontend services."
    )

def build_methodology(doc):
    add_heading_2(doc, "4.3 Methodology & Pipeline Details")
    
    add_heading_3(doc, "1. Database Schema & Multi-Role User Authentication")
    add_body_p(doc, 
        "The relational schema is implemented in app/models.py using Flask-SQLAlchemy. User passwords are cryptographically hashed using "
        "Bcrypt with salted iterations. Role-based access control (RBAC) partitions permissions across four distinct user roles: "
        "student, counsellor, faculty, and admin. The core user entity schema is defined as follows:"
    )
    
    sql_schema = """CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uai_id VARCHAR(64) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL,            -- student, counsellor, faculty, admin
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    department VARCHAR(100),
    designation VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);"""
    add_code_block(doc, sql_schema)
    
    add_heading_3(doc, "2. Clinical Instrument Scoring Formulas & Logic")
    add_body_p(doc, 
        "The algorithmic engine in app/scoring.py computes clinical subscales and severity tiers from raw item responses:"
    )
    
    dass_text = (
        "Depression Score = 2 × ∑ R_i,  for i ∈ {3, 5, 10, 13, 16, 17, 21}\n"
        "Anxiety Score    = 2 × ∑ R_i,  for i ∈ {2, 4, 7, 9, 15, 19, 20}\n"
        "Stress Score     = 2 × ∑ R_i,  for i ∈ {1, 6, 8, 11, 12, 14, 18}"
    )
    add_formula_box(doc, dass_text, label="DASS-21 Subscale Equations (Multiplier = 2 for 42-item equivalence):")
    
    add_body_p(doc, "Standardized DASS-21 Severity Cut-Off Tiers:")
    
    # Severity Table
    tbl_sev = doc.add_table(rows=4, cols=6)
    tbl_sev.style = "Table Grid"
    set_table_borders(tbl_sev)
    col_w = [Inches(1.2), Inches(0.95), Inches(0.95), Inches(0.95), Inches(0.95), Inches(1.0)]
    
    headers_sev = ["Subscale", "Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]
    for idx, w in enumerate(col_w):
        tbl_sev.rows[0].cells[idx].width = w
        format_cell(tbl_sev.rows[0].cells[idx], headers_sev[idx], bg_color="F2F4F8", align=WD_ALIGN_PARAGRAPH.CENTER)
        
    data_sev = [
        ("Depression", "0 – 9", "10 – 13", "14 – 20", "21 – 27", "28+"),
        ("Anxiety", "0 – 7", "8 – 9", "10 – 14", "15 – 19", "20+"),
        ("Stress", "0 – 14", "15 – 18", "19 – 25", "26 – 33", "34+")
    ]
    for r_idx, row_vals in enumerate(data_sev, start=1):
        for c_idx, val in enumerate(row_vals):
            tbl_sev.rows[r_idx].cells[c_idx].width = col_w[c_idx]
            format_cell(tbl_sev.rows[r_idx].cells[c_idx], None, val, 
                        align=WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER)
            if c_idx == 0:
                tbl_sev.rows[r_idx].cells[c_idx].paragraphs[0].runs[0].bold = True

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(4)
    p_space.paragraph_format.space_after = Pt(2)

    bfi_text = (
        "Item Inversion Formula: R_adj = 6 - R_raw  (for reverse-keyed items on 1-5 Likert scale)\n\n"
        "Extraversion       = mean( R1, 6-R6, R11, R16, 6-R21, R26, 6-R31, R36 )\n"
        "Agreeableness      = mean( 6-R2, R7, 6-R12, R17, R22, 6-R27, R32, 6-R37, R42 )\n"
        "Conscientiousness  = mean( R3, 6-R8, R13, 6-R18, 6-R23, R28, R33, R38, 6-R43 )\n"
        "Neuroticism        = mean( R4, 6-R9, R14, R19, 6-R24, R29, 6-R34, R39 )\n"
        "Openness           = mean( R5, R10, R15, R20, R25, R30, 6-R35, R40, 6-R41, R44 )"
    )
    add_formula_box(doc, bfi_text, label="BFI-44 Big Five Personality Trait Formulas:")

    add_body_p(doc, 
        "Automated Emergency Risk Flagging: When determine_risk_level() detects 'Moderate', 'Severe', or 'Extremely Severe' "
        "classifications across any clinical subscale, an automated record is appended to the Flag database table, triggering "
        "instant triage alerts on the counsellor's real-time monitoring interface."
    )

    add_heading_3(doc, "3. Machine Learning Pipeline (ProductivAI)")
    add_body_p(doc, 
        "The ProductivAI predictive analytics service is implemented in ProductivAI/backend/model_training.py. It processes 50,000 synthetic "
        "lifestyle samples modeling student behavioral factors:"
    )
    
    ml_formula = (
        "Feature Input Vector: X = [sleep_hours, study_hours, exercise_mins, screen_time, social_media_mins, mood_score]\n\n"
        "Target Formula: y = 0.25(sleep) + 0.30(study) + 0.15(exercise) - 0.15(screen) - 0.10(social) + 0.15(mood) + ε\n"
        "where ε ~ N(0, 2.5) simulates stochastic real-world variance."
    )
    add_formula_box(doc, ml_formula, label="ProductivAI Synthetic Data Generation & Target Formulation:")
    
    add_body_p(doc, 
        "The training pipeline evaluates both Ordinary Least Squares Linear Regression and Random Forest Regressor models using an 80/20 train-test split. "
        "The trained estimator achieves high R² correlation (> 0.94) and is serialized to disk via Joblib (productivity_model.pkl). The FastAPI service loads "
        "this estimator into memory upon startup, ensuring sub-millisecond REST inference latency during /predict invocations."
    )

def build_technology_stack(doc):
    add_heading_2(doc, "4.4 Technology Stack & Software Ecosystem")
    add_body_p(doc, 
        "The software architecture leverages an enterprise Python backend paired with modern JavaScript frontends. "
        "The table below details all libraries, frameworks, and tools verified across project configuration manifests:"
    )
    
    tbl_tech = doc.add_table(rows=1 + len(TECH_STACK_TABLE_DATA), cols=4)
    tbl_tech.style = "Table Grid"
    set_table_borders(tbl_tech)
    tech_widths = [Inches(1.4), Inches(1.3), Inches(0.9), Inches(2.4)]
    
    headers = ["Layer / Subsystem", "Technology", "Version", "Purpose in Codebase"]
    for idx, w in enumerate(tech_widths):
        tbl_tech.rows[0].cells[idx].width = w
        format_cell(tbl_tech.rows[0].cells[idx], headers[idx], bg_color="F2F4F8", align=WD_ALIGN_PARAGRAPH.CENTER)
        
    for r_idx, (layer, tech, ver, purpose) in enumerate(TECH_STACK_TABLE_DATA, start=1):
        for idx, w in enumerate(tech_widths):
            tbl_tech.rows[r_idx].cells[idx].width = w
        format_cell(tbl_tech.rows[r_idx].cells[0], None, layer, align=WD_ALIGN_PARAGRAPH.LEFT)
        tbl_tech.rows[r_idx].cells[0].paragraphs[0].runs[0].bold = True
        format_cell(tbl_tech.rows[r_idx].cells[1], None, tech, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(tbl_tech.rows[r_idx].cells[2], None, ver, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(tbl_tech.rows[r_idx].cells[3], None, purpose, align=WD_ALIGN_PARAGRAPH.LEFT)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(6)
    p_space.paragraph_format.space_after = Pt(2)

def build_results_and_discussion(doc):
    add_heading_1(doc, "5. Results & Discussion")
    
    add_heading_2(doc, "5.1 System Accomplishments")
    add_body_p(doc, 
        "Execution of the unified launcher script (launch_all.bat) brings all microservices and frontend SPAs online simultaneously. "
        "The system accomplishes the following verified operational outcomes:"
    )
    
    add_bullet_item(doc, "1. Integrated Web Portal Execution: ", 
        "Serves the primary Flask application on port 5000, presenting student screening, faculty assessment dashboards, and administrative controls."
    )
    add_bullet_item(doc, "2. Dynamic React SPA Bootstrapping: ", 
        "The Counsellor Dashboard injects live database queries into global window objects (window.__FLASK_KPIS__, window.__FLASK_FLAGGED_STUDENTS__), "
        "delivering instant UI hydration without client-side authentication latency."
    )
    add_bullet_item(doc, "3. Automated Risk Triage: ", 
        "Submission of student assessment responses immediately triggers run_all_scores(), updates severity metrics, and logs emergency flags for counsellor intervention."
    )
    add_bullet_item(doc, "4. Instant Diagnostic Export: ", 
        "Enables one-click generation of institutional PDF diagnostic reports using ReportLab, formatted with student demographics, severity charts, and legal disclaimers."
    )
    add_bullet_item(doc, "5. Real-Time ML Productivity Predictions: ", 
        "The ProductivAI FastAPI service on port 8000 processes daily lifestyle indicators via /predict, returning a 0–100 score, factor contribution breakdowns, and contextual AI advice."
    )
    
    # Embed Workflow Image
    if os.path.exists(WORKFLOW_IMG_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(WORKFLOW_IMG_PATH, width=Inches(5.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run("Figure 2: Operational Workflow and Cross-Service Execution Pipeline.")
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    add_heading_2(doc, "5.2 Advantages of the Approach")
    add_bullet_item(doc, "• Hybrid Integration Strategy: ", 
        "Bootstrapping compiled Vite static bundles into Jinja2 templates combines the high initial load speed of server-rendered apps with the rich interactivity of modern React SPAs."
    )
    add_bullet_item(doc, "• Strict Clinical Accuracy: ", 
        "Utilizing mathematically validated scoring formulas and explicit reverse-key transformations ensures diagnostic precision across psychological instruments."
    )
    add_bullet_item(doc, "• Fail-Safe Offline Capability: ", 
        "The standalone Tkinter Quiz App ensures psychometric tests can proceed smoothly even in offline laboratory environments without network access."
    )
    add_bullet_item(doc, "• Modular Microservice Design: ", 
        "Decoupling the machine learning inference engine (ProductivAI) from the core clinical database (PsychePortal) ensures heavy matrix computations do not block critical student screening requests."
    )

    add_heading_2(doc, "5.3 Limitations")
    add_bullet_item(doc, "• Lack of Automated Unit Tests: ", 
        "The repository currently relies on manual verification scripts (check_users.py, verify_portal.py) rather than an automated CI/CD pytest test suite."
    )
    add_bullet_item(doc, "• Hardcoded Development Secrets: ", 
        "Default development fallback secrets (e.g. SECRET_KEY in config.py) require migration to enterprise secret management vaults before production cloud deployment."
    )
    add_bullet_item(doc, "• Synthetic Data Training: ", 
        "ProductivAI's regression models were trained on mathematically simulated lifestyle data rather than longitudinal real-world student behavioral logs."
    )
    add_bullet_item(doc, "• Local SQLite File Locking: ", 
        "Default local execution uses SQLite, which is prone to file-locking contention under high concurrent write loads compared to production PostgreSQL."
    )

    add_heading_2(doc, "5.4 Future Scope")
    add_bullet_item(doc, "• WebSocket Real-Time Alerts: ", 
        "Implementing Socket.IO WebSockets to replace HTTP polling, delivering instantaneous counsellor notification when emergency flags trigger."
    )
    add_bullet_item(doc, "• Longitudinal Trend Analysis: ", 
        "Extending the AssessmentScore model to visualize student psychological trajectories across consecutive semesters using predictive time-series charts."
    )
    add_bullet_item(doc, "• Production Cloud Containerization: ", 
        "Finalizing Dockerfile and Docker Compose configurations for seamless cloud deployment via Kubernetes or Render."
    )
    add_bullet_item(doc, "• Real-World Model Fine-Tuning: ", 
        "Collecting opt-in, anonymized student academic performance and routine tracking data to fine-tune ProductivAI's predictive weights."
    )

def build_conclusion_and_references(doc):
    add_heading_1(doc, "6. Conclusion")
    add_body_p(doc, 
        "The AI Internship project successfully designed, implemented, and integrated two production-grade software platforms: "
        "the UAi PsychePortal clinical assessment suite and the ProductivAI lifestyle productivity engine. The project realized "
        "significant milestones across four engineering domains:"
    )
    add_bullet_item(doc, "1. Full-Stack Web Engineering: ", 
        "Engineered responsive, highly performant web applications combining Flask, SQLAlchemy, FastAPI, React 18, TailwindCSS, and Vite."
    )
    add_bullet_item(doc, "2. Clinical Data Systems: ", 
        "Automated complex scoring mathematics, threshold triage, and dynamic multi-page ReportLab PDF generation for standardized psychological instruments."
    )
    add_bullet_item(doc, "3. Predictive Analytics: ", 
        "Developed, trained, serialized, and deployed high-accuracy machine learning regression pipelines with sub-millisecond API response latency."
    )
    add_bullet_item(doc, "4. Architectural Integration: ", 
        "Unified microservices, standalone desktop clients, and single-page apps into a cohesive, multi-process launchable ecosystem."
    )
    
    add_heading_1(doc, "7. References")
    
    references = [
        "[1] S. Grinberg, Flask Web Development: Developing Web Applications with Python, 2nd ed. Sebastopol, CA: O'Reilly Media, 2018.",
        "[2] S. Raschka and V. Mirjalili, Python Machine Learning, 3rd ed. Birmingham, UK: Packt Publishing, 2019.",
        "[3] P. S. Lovibond and S. H. Lovibond, \"The structure of negative emotional states: Comparison of the Depression Anxiety Stress Scales (DASS) with the Beck Depression and Anxiety Inventories,\" Behaviour Research and Therapy, vol. 33, no. 3, pp. 335–343, 1995.",
        "[4] O. P. John, E. M. Donahue, and R. L. Kentle, The Big Five Inventory--Versions 4a and 54, Berkeley, CA: University of California, Berkeley, Institute of Personality and Social Research, 1991.",
        "[5] ReportLab Inc., ReportLab PDF Library User Guide, Version 4.1.0, 2024. [Online]. Available: https://www.reportlab.com/docs/reportlab-userguide.pdf",
        "[6] Scikit-learn Developers, Scikit-learn: Machine Learning in Python, 2024. [Online]. Available: https://scikit-learn.org/stable/documentation.html",
        "[7] FastAPI Developers, FastAPI Framework Documentation, 2024. [Online]. Available: https://fastapi.tiangolo.com/",
        "[8] Meta Platforms Inc., React - A JavaScript library for building user interfaces, 2024. [Online]. Available: https://react.dev/"
    ]
    
    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r = p_ref.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    doc.add_page_break()

def build_part_2_divider(doc):
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(40)
    p_div.paragraph_format.space_after = Pt(12)
    r = p_div.add_run("PART 2: SUMMER INTERNSHIP WEEKLY REPORTS")
    r.font.name = "Times New Roman"
    r.font.size = Pt(18)
    r.bold = True
    r.font.color.rgb = RGBColor(0x0F, 0x2D, 0x59)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(20)
    r = p_sub.add_run(
        "Official Weekly Progress Reports (Week 1 through Week 6)\n"
        "Submitted to: School of Ai & Future Technologies, Universal Ai University\n"
        "Faculty Mentor: Prof. Rajesh Bhise | Department: Ai Cell"
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
    
    doc.add_page_break()

def main():
    print("Initializing comprehensive document from university template...")
    doc = docx.Document(TEMPLATE_PATH)
    
    # Clear initial template body elements except the last sectPr
    body = doc._element.body
    for child in list(body)[:-1]:
        body.remove(child)
        
    print("Building Part 1: University Project Report...")
    build_cover_page(doc)
    build_executive_summary(doc)
    build_table_of_contents(doc)
    build_introduction(doc)
    build_system_architecture(doc)
    build_methodology(doc)
    build_technology_stack(doc)
    build_results_and_discussion(doc)
    build_conclusion_and_references(doc)
    
    print("Building Part 2: Weekly Progress Reports (Weeks 1 to 6)...")
    build_part_2_divider(doc)
    
    for idx, data in enumerate(WEEKLY_DATA):
        print(f"  Adding {data['week_title']} ({data['week_no']})...")
        build_weekly_report_section(doc, data, is_first=(idx == 0))
        
    print(f"Saving final master document to {OUTPUT_DOC_PATH}...")
    doc.save(OUTPUT_DOC_PATH)
    
    print(f"Copying to Downloads folder: {OUTPUT_DOWNLOADS_PATH}...")
    shutil.copy(OUTPUT_DOC_PATH, OUTPUT_DOWNLOADS_PATH)
    
    print("Build complete! Both documents generated successfully.")

if __name__ == "__main__":
    main()
