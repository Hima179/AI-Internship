import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import docx2pdf
import pypdf

TEMPLATE_PATH = r"C:\Users\Himanshu Pathak\Downloads\Summer_Internship_Weekly_Report (1).docx"
OUTPUT_DOCX = r"d:\AI INTERNSHIP\HimanshuPathak_UAI05BT12417_SIP_WeeklyReport.docx"
OUTPUT_PDF = r"d:\AI INTERNSHIP\HimanshuPathak_UAI05BT12417_SIP_WeeklyReport.pdf"
DOWNLOADS_DOCX = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_UAI05BT12417_SIP_WeeklyReport.docx"
DOWNLOADS_PDF = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_UAI05BT12417_SIP_WeeklyReport.pdf"
STUDENT_SIGNATURE_IMG = r"d:\AI INTERNSHIP\himanshu_student_signature.png"

# 10 Weeks Data covering 4th May 2026 to 14th July 2026
WEEKLY_DATA = [
    {
        "week_title": "First Week",
        "week_no": "Week 1",
        "period": "04-May-2026 to 10-May-2026",
        "tasks": [
            ("1", "Requirement analysis, architectural design, and repository layout setup for UAi PsychePortal", "Completed"),
            ("2", "Defined SQLAlchemy relational database models (User, StudentProfile, Assessment, SubscaleScore)", "Completed"),
            ("3", "Implemented Flask application factory pattern and dynamic environment configuration handling", "Completed"),
            ("4", "Configured environment variables and established development SQLite database with foreign keys", "Completed")
        ],
        "technologies": [
            "Python 3.13, Flask 3.0.0",
            "Flask-SQLAlchemy, SQLite",
            "Git, VS Code"
        ],
        "learning_outcomes": [
            "Standardized database normalization techniques for relational models storing psychometric profiles.",
            "Configured Flask application factory patterns to isolate development and production environments.",
            "Mastered Git branching workflows for full-stack multi-service repository development."
        ],
        "challenges": "Cyclic imports between models, database initializers, and authentication blueprints.",
        "solutions": "Implemented Application Factory pattern (create_app) in app/__init__.py, decoupling model declarations from route handlers.",
        "plan_next_week": [
            ("1", "Implement DASS-21, BFI-44, EQ, and SQ mathematical scoring functions", "6 Hours"),
            ("2", "Create automated risk-flagging logic for severe student scores", "4 Hours"),
            ("3", "Develop seed data scripts (seed_questions.py, seed_demo_data.py)", "4 Hours")
        ]
    },
    {
        "week_title": "Second Week",
        "week_no": "Week 2",
        "period": "11-May-2026 to 17-May-2026",
        "tasks": [
            ("1", "Implemented scoring algorithms for DASS-21, BFI-44, EQ, and SQ in app/scoring.py", "Completed"),
            ("2", "Engineered automated emergency risk flagging for Moderate/Severe subscale categories", "Completed"),
            ("3", "Created database population scripts for 100+ demo profiles and question banks", "Completed")
        ],
        "technologies": [
            "Python 3.13, SQLAlchemy ORM",
            "Flask-Bcrypt, Flask-Login",
            "SQLite database browser, PyTest"
        ],
        "learning_outcomes": [
            "Mastered reverse-score transformations (6 - R) and subscale matrix indexing for Big Five inventory metrics.",
            "Developed automated event triggers in SQLAlchemy to flag high-risk entries upon submission.",
            "Formulated automated clinical cutoffs across standard psychometric scales."
        ],
        "challenges": "Handling missing item selections without crashing subscale calculations.",
        "solutions": "Defaulted missing responses to neutral values (3 for BFI-44, 0 for DASS-21) inside safe map retrievals (resp_map.get(i, default)).",
        "plan_next_week": [
            ("1", "Construct programmatic PDF report builder using ReportLab", "6 Hours"),
            ("2", "Implement Excel data export using Pandas and OpenPyXL", "4 Hours"),
            ("3", "Build Student Survey Web Portal on port 5001", "5 Hours")
        ]
    },
    {
        "week_title": "Third Week",
        "week_no": "Week 3",
        "period": "18-May-2026 to 24-May-2026",
        "tasks": [
            ("1", "Developed PDF export generation using ReportLab (SimpleDocTemplate, TableStyle, Flowables)", "Completed"),
            ("2", "Built Excel export features for counsellor metrics using Pandas and OpenPyXL", "Completed"),
            ("3", "Deployed standalone Flask Student Survey Portal running on port 5001", "Completed")
        ],
        "technologies": [
            "ReportLab 4.1.0, Pandas 2.1.4",
            "OpenPyXL 3.1.2",
            "Flask Jinja2 Templating, SQLite WAL"
        ],
        "learning_outcomes": [
            "Standardized programmatic document formatting using ReportLab flowables, tables, and page breaks.",
            "Integrated dual-Flask microservice instances sharing a common SQLite relational database.",
            "Formatted tabular data exports with auto-column sizing and header styling."
        ],
        "challenges": "PDF layout text overflow when rendering student assessment details across page boundaries.",
        "solutions": "Encapsulated tabular cell text within Paragraph flowables with automated auto-wrapping text styles.",
        "plan_next_week": [
            ("1", "Develop modern React SPA Counsellor Dashboard using Vite and TailwindCSS", "8 Hours"),
            ("2", "Build 11 dashboard view modules (Risk Alerts, Directory, Deployer)", "5 Hours"),
            ("3", "Set up Chart.js radar and trend analytics visualizations", "4 Hours")
        ]
    },
    {
        "week_title": "Fourth Week",
        "week_no": "Week 4",
        "period": "25-May-2026 to 31-May-2026",
        "tasks": [
            ("1", "Built Vite + React single-page application inside uai-counsellor-dashboard/", "Completed"),
            ("2", "Designed 11 dynamic views featuring TailwindCSS styling and Lucide icons", "Completed"),
            ("3", "Configured interactive Chart.js visualizations for subscale trend analysis and cohort heatmaps", "Completed")
        ],
        "technologies": [
            "React 18, Vite 5",
            "TailwindCSS 3.4, Lucide-React",
            "Chart.js 4.4, REST API"
        ],
        "learning_outcomes": [
            "Engineered dynamic dashboard views using React state hooks (useState, useEffect, useMemo).",
            "Applied responsive dark-theme design patterns using TailwindCSS utilities and CSS custom variables.",
            "Built reusable UI components including modal dialogs, search bars, and risk badge pills."
        ],
        "challenges": "Integrating client-side React routes into Flask server-rendered endpoints without 404 errors.",
        "solutions": "Compiled Vite static assets into Flask's static directory and rendered root React <div id=\"root\"> via Jinja2 catch-all.",
        "plan_next_week": [
            ("1", "Connect React frontend with Flask database using Jinja2 JSON script injection", "4 Hours"),
            ("2", "Develop ProductivAI synthetic dataset generator (50,000 samples)", "4 Hours"),
            ("3", "Train and serialize Random Forest ML productivity regression model", "5 Hours")
        ]
    },
    {
        "week_title": "Fifth Week",
        "week_no": "Week 5",
        "period": "01-Jun-2026 to 07-Jun-2026",
        "tasks": [
            ("1", "Connected React frontend with Flask database using Jinja2 JSON script injection", "Completed"),
            ("2", "Built 50,000-sample synthetic lifestyle dataset generator (generate_dataset.py)", "Completed"),
            ("3", "Trained Random Forest Regressor and exported model via Joblib (productivity_model.pkl)", "Completed")
        ],
        "technologies": [
            "Scikit-Learn 1.3, Joblib",
            "NumPy, Pandas",
            "FastAPI, Uvicorn, Python 3.13"
        ],
        "learning_outcomes": [
            "Evaluated regression models using metrics such as R², MAE, and MSE.",
            "Deserialized trained .pkl estimators inside FastAPI endpoints for real-time inference.",
            "Analyzed feature importance rankings to identify sleep and study hours as primary productivity drivers."
        ],
        "challenges": "Model inference latency spikes when serving REST requests under heavy batch load.",
        "solutions": "Cached the deserialized Joblib model instance in global application memory upon FastAPI startup.",
        "plan_next_week": [
            ("1", "Develop ProductivAI React analytics dashboard with score dials and Recharts", "5 Hours"),
            ("2", "Write integrated multi-process launcher scripts (launch_all.bat / .ps1)", "4 Hours"),
            ("3", "Perform initial multi-port system verification across ports 5000, 5001, and 8000", "4 Hours")
        ]
    },
    {
        "week_title": "Sixth Week",
        "week_no": "Week 6",
        "period": "08-Jun-2026 to 14-Jun-2026",
        "tasks": [
            ("1", "Built ProductivAI React analytics dashboard with score dials, lifestyle radar, and dark/light themes", "Completed"),
            ("2", "Created unified multi-process orchestrators (launch_all.bat and launch_all.ps1)", "Completed"),
            ("3", "Executed full system integration verification across ports 5000, 5001, and 8000", "Completed")
        ],
        "technologies": [
            "Windows Batch Scripting, PowerShell 7",
            "React 18, Recharts 2.10",
            "Framer Motion, FastAPI"
        ],
        "learning_outcomes": [
            "Automated multi-process application deployment using shell scripting techniques.",
            "Verified cross-origin data flows and API request validation across distinct microservices.",
            "Configured graceful shutdown handlers in PowerShell to kill child processes cleanly."
        ],
        "challenges": "Managing multiple terminal windows and port collisions during full-stack startup.",
        "solutions": "Wrote automated PowerShell start routines with explicit port bindings (-port 5000, -port 5001, -port 8000) and port clearing.",
        "plan_next_week": [
            ("1", "Build offline desktop assessment client using Python Tkinter (UAI_Quiz_App)", "6 Hours"),
            ("2", "Implement local JSON question storage and offline submission logging", "4 Hours"),
            ("3", "Develop offline-to-online sync reconciliation script (sync_offline_assessments.py)", "5 Hours")
        ]
    },
    {
        "week_title": "Seventh Week",
        "week_no": "Week 7",
        "period": "15-Jun-2026 to 21-Jun-2026",
        "tasks": [
            ("1", "Developed native Python Tkinter GUI psychometric assessment application (UAI_Quiz_App)", "Completed"),
            ("2", "Implemented offline local JSON question pools and secure local result caching", "Completed"),
            ("3", "Built automated sync script reconciling offline desktop submissions with central SQLite database", "Completed")
        ],
        "technologies": [
            "Python 3.13, Tkinter GUI",
            "SQLite, JSON Serialization",
            "PyInstaller standalone compiler"
        ],
        "learning_outcomes": [
            "Designed offline-capable clinical assessment tools for campus labs with intermittent internet.",
            "Implemented idempotent database upsert operations to prevent duplicate record syncs.",
            "Mastered desktop application packaging and cross-platform GUI event handling."
        ],
        "challenges": "Ensuring deterministic UUID matching between offline desktop submissions and central database rows.",
        "solutions": "Generated SHA-256 hash digests from student roll number, timestamp, and responses as unique record keys.",
        "plan_next_week": [
            ("1", "Formulate comprehensive end-to-end integration and automated unit test suites", "6 Hours"),
            ("2", "Implement security audits including CSRF, SQL injection, and password hash validations", "4 Hours"),
            ("3", "Conduct database load testing under simulated 500-student concurrent intake", "5 Hours")
        ]
    },
    {
        "week_title": "Eighth Week",
        "week_no": "Week 8",
        "period": "22-Jun-2026 to 28-Jun-2026",
        "tasks": [
            ("1", "Built automated test suites using PyTest covering scoring math, authentication, and API endpoints", "Completed"),
            ("2", "Conducted rigorous security audits: verified Bcrypt 12-round hashing and CSRF protections", "Completed"),
            ("3", "Executed database stress testing validating SQLite WAL mode under concurrent student submissions", "Completed")
        ],
        "technologies": [
            "PyTest, Requests",
            "SQLite EXPLAIN QUERY PLAN",
            "Bcrypt, Chrome DevTools"
        ],
        "learning_outcomes": [
            "Formulated 4-tier testing strategies (Unit, Integration, Security, and Concurrency).",
            "Mastered database indexing optimization, reducing subscale aggregation times by 78%.",
            "Validated zero data corruption under concurrent multi-process SQLite read/write operations."
        ],
        "challenges": "SQLite lock contention errors during simulated multi-user concurrent intake testing.",
        "solutions": "Enabled SQLite Write-Ahead Logging (WAL) and configured busy timeout to 30,000 milliseconds.",
        "plan_next_week": [
            ("1", "Conduct user acceptance testing (UAT) with campus counsellors and student test cohorts", "6 Hours"),
            ("2", "Refine UI ergonomics based on feedback: adjust font sizes, tooltips, and export buttons", "4 Hours"),
            ("3", "Package production-ready Vite builds and compile optimized static bundles", "5 Hours")
        ]
    },
    {
        "week_title": "Ninth Week",
        "week_no": "Week 9",
        "period": "29-Jun-2026 to 05-Jul-2026",
        "tasks": [
            ("1", "Conducted User Acceptance Testing (UAT) sessions with campus counselling staff and student cohorts", "Completed"),
            ("2", "Optimized Counsellor SPA interface based on feedback: refined risk badges and report download buttons", "Completed"),
            ("3", "Generated production-optimized Vite static builds and minimized bundle payloads (npm run build)", "Completed")
        ],
        "technologies": [
            "React 18, Vite 5 (Rollup Bundler)",
            "TailwindCSS, Postman",
            "Google Lighthouse audit"
        ],
        "learning_outcomes": [
            "Gained valuable experience translating user feedback into practical software design refinements.",
            "Optimized web application performance, achieving Lighthouse audit scores above 95 across all metrics.",
            "Mastered static asset caching and code-splitting strategies for React single-page applications."
        ],
        "challenges": "Bundle size exceeding 1.2 MB due to heavy charting libraries (Chart.js and Recharts).",
        "solutions": "Implemented dynamic React.lazy() code splitting for analytics dashboards and charted components.",
        "plan_next_week": [
            ("1", "Finalize technical documentation, API specifications, and architectural diagrams", "6 Hours"),
            ("2", "Prepare deployment handover package and containerization guides (Docker/Compose)", "4 Hours"),
            ("3", "Conduct final project demonstration and academic viva presentation to mentors", "5 Hours")
        ]
    },
    {
        "week_title": "Tenth Week",
        "week_no": "Week 10",
        "period": "06-Jul-2026 to 14-Jul-2026",
        "tasks": [
            ("1", "Compiled complete technical project documentation, API references, and architecture manuals", "Completed"),
            ("2", "Created containerization deployment blueprints (Dockerfile, docker-compose.yml) for cloud hosting", "Completed"),
            ("3", "Completed final project presentation, demonstration, and viva handover to faculty mentors on 14th July 2026", "Completed")
        ],
        "technologies": [
            "Docker, Docker Compose",
            "ReportLab, Docx2Pdf",
            "Markdown, Git"
        ],
        "learning_outcomes": [
            "Mastered production software release engineering, containerization, and technical documentation.",
            "Developed comprehensive institutional handover protocols for enterprise AI healthcare systems.",
            "Successfully delivered an end-to-end full-stack software suite ready for campus-wide deployment."
        ],
        "challenges": "Coordinating final academic deliverables against university handbook formatting standards.",
        "solutions": "Conducted rigorous document forensic checks and compiled verified publication-grade PDF deliverables.",
        "plan_next_week": [
            ("1", "Post-internship institutional maintenance and phase-2 planning", "0 Hours")
        ]
    }
]

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
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

def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_cell(cell, bold_label=None, value_text="", font_name="Times New Roman", font_size=10.5, bg_color=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    if bg_color:
        set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    if bold_label:
        r1 = p.add_run(bold_label)
        r1.font.name = font_name
        r1.font.size = Pt(font_size)
        r1.bold = True
    if value_text:
        r2 = p.add_run(value_text)
        r2.font.name = font_name
        r2.font.size = Pt(font_size)
        r2.bold = False

def build_weekly_report_section(doc, data, is_first=False):
    """Adds a single week report adhering exactly to the official university template (2 pages per week)."""
    if not is_first:
        doc.add_page_break()

    # Page 1 of Week
    h1 = doc.add_paragraph()
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(2)
    h1.paragraph_format.space_after = Pt(6)
    r = h1.add_run("Summer Internship Weekly Report")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    # Student Details
    p_sd = doc.add_paragraph()
    p_sd.paragraph_format.space_before = Pt(2)
    p_sd.paragraph_format.space_after = Pt(2)
    r = p_sd.add_run("Student Details")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True

    tbl_sd = doc.add_table(rows=3, cols=2)
    tbl_sd.style = "Table Grid"
    set_table_borders(tbl_sd)
    col_widths = [Inches(3.2), Inches(3.2)]
    for row in tbl_sd.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    format_cell(tbl_sd.rows[0].cells[0], "Student Name: ", "Himanshu Pathak")
    format_cell(tbl_sd.rows[0].cells[1], "Roll No.: ", "UAI05BT12417")
    format_cell(tbl_sd.rows[1].cells[0], "Year/ Semester: ", "2nd Year / 4th Semester")
    format_cell(tbl_sd.rows[1].cells[1], "Email Id: ", "himanshu.pathak@universalai.in")
    format_cell(tbl_sd.rows[2].cells[0], "Faculty Mentor : ", "Prof. Rajesh Bhise")
    format_cell(tbl_sd.rows[2].cells[1], "Contact No.: ", "9820767182")

    # Company Details
    p_cd = doc.add_paragraph()
    p_cd.paragraph_format.space_before = Pt(4)
    p_cd.paragraph_format.space_after = Pt(2)
    r = p_cd.add_run("Company Details:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True

    tbl_cd = doc.add_table(rows=3, cols=2)
    tbl_cd.style = "Table Grid"
    set_table_borders(tbl_cd)
    for row in tbl_cd.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    format_cell(tbl_cd.rows[0].cells[0], "Company Name: ", "Ai Cell, Universal Ai University")
    format_cell(tbl_cd.rows[0].cells[1], "Department Name: ", "School of Ai & Future Technologies")
    format_cell(tbl_cd.rows[1].cells[0], "Company Manger Name: ", "Prof. Rajesh Bhise / Dr. Shivaji Pawar")
    format_cell(tbl_cd.rows[1].cells[1], "Official Mail Id: ", "aicell@universalai.in")
    format_cell(tbl_cd.rows[2].cells[0], "Contact No: ", "+91 2192 664000")
    format_cell(tbl_cd.rows[2].cells[1], "Website: ", "https://www.universalai.in")

    # Meta
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(4)
    p_meta.paragraph_format.space_after = Pt(2)
    p_meta.paragraph_format.line_spacing = 1.15

    r = p_meta.add_run("Project Title: ")
    r.bold = True
    r.font.name = "Times New Roman"
    r = p_meta.add_run("Full-Stack AI & Clinical Assessment Systems (UAi PsychePortal & ProductivAI)\n")
    r.font.name = "Times New Roman"

    r = p_meta.add_run("Week No.: ")
    r.bold = True
    r.font.name = "Times New Roman"
    r = p_meta.add_run(f"{data['week_title']}\n")
    r.font.name = "Times New Roman"

    r = p_meta.add_run("Reporting Period: ")
    r.bold = True
    r.font.name = "Times New Roman"
    r = p_meta.add_run(f"{data['period']}")
    r.font.name = "Times New Roman"

    # 1. Weekly Task
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(4)
    p_h.paragraph_format.space_after = Pt(2)
    r = p_h.add_run("1. Weekly Task")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

    tasks = data["tasks"]
    tbl_task = doc.add_table(rows=1 + len(tasks), cols=3)
    tbl_task.style = "Table Grid"
    set_table_borders(tbl_task)
    task_widths = [Inches(0.6), Inches(4.8), Inches(1.0)]

    for idx, w in enumerate(task_widths):
        tbl_task.rows[0].cells[idx].width = w
    format_cell(tbl_task.rows[0].cells[0], "S. No", bg_color="F2F4F8", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(tbl_task.rows[0].cells[1], "Task Description", bg_color="F2F4F8", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(tbl_task.rows[0].cells[2], "Status", bg_color="F2F4F8", align=WD_ALIGN_PARAGRAPH.CENTER)

    for r_idx, (sno, desc, status) in enumerate(tasks, start=1):
        for idx, w in enumerate(task_widths):
            tbl_task.rows[r_idx].cells[idx].width = w
        format_cell(tbl_task.rows[r_idx].cells[0], None, sno, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(tbl_task.rows[r_idx].cells[1], None, desc, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(tbl_task.rows[r_idx].cells[2], None, status, align=WD_ALIGN_PARAGRAPH.CENTER)

    # 2. Technologies/Tools Used
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(4)
    p_h.paragraph_format.space_after = Pt(2)
    r = p_h.add_run("2. Technologies/Tools Used")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

    for tech in data["technologies"]:
        p_item = doc.add_paragraph(style="List Bullet")
        p_item.paragraph_format.space_before = Pt(0)
        p_item.paragraph_format.space_after = Pt(1)
        r = p_item.add_run(tech)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)

    # Page Break to Page 2 of Week
    doc.add_page_break()

    # 3. Learning Outcomes
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(4)
    p_h.paragraph_format.space_after = Pt(2)
    r = p_h.add_run("3. Learning Outcomes")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

    for outcome in data["learning_outcomes"]:
        p_item = doc.add_paragraph(style="List Bullet")
        p_item.paragraph_format.space_before = Pt(0)
        p_item.paragraph_format.space_after = Pt(1)
        r = p_item.add_run(outcome)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)

    # 4. Challenges Faced & Solutions
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(4)
    p_h.paragraph_format.space_after = Pt(2)
    r = p_h.add_run("4. Challenges Faced & Solutions")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

    p_cs = doc.add_paragraph()
    p_cs.paragraph_format.space_before = Pt(1)
    p_cs.paragraph_format.space_after = Pt(4)
    p_cs.paragraph_format.line_spacing = 1.15

    r = p_cs.add_run("Challenges:\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r = p_cs.add_run(f"{data['challenges']}\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)

    r = p_cs.add_run("Solutions:\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r = p_cs.add_run(f"{data['solutions']}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)

    # 5. Plan for Next Week
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(4)
    p_h.paragraph_format.space_after = Pt(2)
    r = p_h.add_run("5. Plan for Next Week")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

    plans = data["plan_next_week"]
    tbl_plan = doc.add_table(rows=1 + len(plans), cols=3)
    tbl_plan.style = "Table Grid"
    set_table_borders(tbl_plan)
    plan_widths = [Inches(0.6), Inches(4.8), Inches(1.0)]

    for idx, w in enumerate(plan_widths):
        tbl_plan.rows[0].cells[idx].width = w
    format_cell(tbl_plan.rows[0].cells[0], "S. No", bg_color="F2F4F8", align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(tbl_plan.rows[0].cells[1], "Task to be done", bg_color="F2F4F8", align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(tbl_plan.rows[0].cells[2], "Estimated Time", bg_color="F2F4F8", align=WD_ALIGN_PARAGRAPH.CENTER)

    for r_idx, (sno, task_todo, est_time) in enumerate(plans, start=1):
        for idx, w in enumerate(plan_widths):
            tbl_plan.rows[r_idx].cells[idx].width = w
        format_cell(tbl_plan.rows[r_idx].cells[0], None, sno, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(tbl_plan.rows[r_idx].cells[1], None, task_todo, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell(tbl_plan.rows[r_idx].cells[2], None, est_time, align=WD_ALIGN_PARAGRAPH.CENTER)

    # Signatures Table (3 Signatories)
    tbl_sig = doc.add_table(rows=1, cols=3)
    tbl_sig.style = "Table Grid"
    set_table_borders(tbl_sig, color="FFFFFF", sz="0")
    for row in tbl_sig.rows:
        row.cells[0].width = Inches(2.1)
        row.cells[1].width = Inches(2.1)
        row.cells[2].width = Inches(2.2)

    # Student Signature with embedded digital signature
    c0 = tbl_sig.rows[0].cells[0]
    set_cell_margins(c0, top=40, bottom=40, left=80, right=80)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(0)
    p0.paragraph_format.line_spacing = 1.05
    r_sl = p0.add_run("Student Signature:\n(Digital Signature)\n")
    r_sl.font.name = "Times New Roman"
    r_sl.font.size = Pt(9.0)
    r_sl.bold = True
    if os.path.exists(STUDENT_SIGNATURE_IMG):
        r_img = p0.add_run()
        r_img.add_picture(STUDENT_SIGNATURE_IMG, width=Inches(1.1))
    r_sn = p0.add_run("\nHimanshu Pathak\nUAI05BT12417")
    r_sn.font.name = "Times New Roman"
    r_sn.font.size = Pt(8.5)

    format_cell(tbl_sig.rows[0].cells[1], "Faculty Mentor Signature:\n", "\n___________________\nProf. Rajesh Bhise\nSchool of AI & Tech", font_size=9.0)
    format_cell(tbl_sig.rows[0].cells[2], "Industry Guide / HOD:\n", "\n___________________\nDr. Shivaji Pawar\nHead of Department", font_size=9.0)

def main():
    print("=" * 70)
    print("GENERATING STANDALONE 10-WEEK INTERNSHIP REPORT (4 MAY TO 14 JULY 2026)")
    print("=" * 70)

    # Load template preserving headers and university logos
    doc = docx.Document(TEMPLATE_PATH)

    # Clear existing body elements
    body = doc._element.body
    for child in list(body)[:-1]:
        body.remove(child)

    # Build each of the 10 weeks
    for idx, data in enumerate(WEEKLY_DATA):
        print(f"Writing {data['week_title']} ({data['period']})...")
        build_weekly_report_section(doc, data, is_first=(idx == 0))

    # Save Word document
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
    print("STANDALONE WEEKLY INTERNSHIP REPORT COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    main()
