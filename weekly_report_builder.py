import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import shutil
import os

TEMPLATE_PATH = r"C:\Users\Himanshu Pathak\Downloads\Summer_Internship_Weekly_Report (1).docx"
ARCH_IMG_PATH = r"d:\AI INTERNSHIP\system_architecture_diagram.png"
WORKFLOW_IMG_PATH = r"d:\AI INTERNSHIP\workflow_pipeline_diagram.png"

WEEKLY_DATA = [
    {
        "week_title": "First Week",
        "week_no": "Week 1",
        "period": "4-May-2026 to 9-May-2026",
        "tasks": [
            ("1", "Requirement analysis, architectural design, and repository layout setup", "Completed"),
            ("2", "Defined SQLAlchemy database schema (User, StudentProfile, Assessment)", "Completed"),
            ("3", "Implemented Flask factory pattern and dynamic configuration handling", "Completed")
        ],
        "technologies": [
            "Python 3.13, Flask 3.0.0",
            "Flask-SQLAlchemy, SQLite",
            "Git, VS Code"
        ],
        "learning_outcomes": [
            "Standardized database normalization techniques for relational models storing psychometric profiles.",
            "Configured Flask application factory patterns to isolate development and production environments."
        ],
        "challenges": "Avoid cyclic imports between models, database initializers, and authentication blueprints.",
        "solutions": "Implemented the Application Factory pattern (create_app) in app/__init__.py, decoupling model declarations from route handlers.",
        "plan_next_week": [
            ("1", "Implement DASS-21, BFI-44, EQ, and SQ mathematical scoring functions", "6 Hours"),
            ("2", "Create automated risk-flagging logic for severe student scores", "4 Hours"),
            ("3", "Develop seed data scripts (seed_questions.py, seed_demo_data.py)", "4 Hours")
        ]
    },
    {
        "week_title": "Second Week",
        "week_no": "Week 2",
        "period": "11-May-2026 to 16-May-2026",
        "tasks": [
            ("1", "Implemented scoring algorithms for DASS-21, BFI-44, EQ, and SQ in app/scoring.py", "Completed"),
            ("2", "Engineered automated emergency risk flagging for Moderate/Severe subscale categories", "Completed"),
            ("3", "Created database population scripts for 100+ demo profiles and question banks", "Completed")
        ],
        "technologies": [
            "Python 3.13, SQLAlchemy ORM",
            "Flask-Bcrypt, Flask-Login",
            "SQLite database browser"
        ],
        "learning_outcomes": [
            "Mastered reverse-score transformations (6 - R) and subscale matrix indexing for Big Five inventory metrics.",
            "Developed automated event triggers in SQLAlchemy to flag high-risk entries upon submission."
        ],
        "challenges": "Handling missing item selections without crashing subscale calculations.",
        "solutions": "Defaulted missing responses to neutral values (3) for BFI-44 and 0 for DASS-21 inside safe map retrievals (resp_map.get(i, default)).",
        "plan_next_week": [
            ("1", "Construct programmatic PDF report builder using ReportLab", "6 Hours"),
            ("2", "Implement Excel data export using Pandas and OpenPyXL", "4 Hours"),
            ("3", "Build Student Survey Web Portal (student-survey-portal/app.py)", "5 Hours")
        ]
    },
    {
        "week_title": "Third Week",
        "week_no": "Week 3",
        "period": "18-May-2026 to 23-May-2026",
        "tasks": [
            ("1", "Developed PDF export generation using ReportLab (SimpleDocTemplate, TableStyle)", "Completed"),
            ("2", "Built Excel export features for counsellor metrics using Pandas and OpenPyXL", "Completed"),
            ("3", "Deployed standalone Flask Student Survey Portal running on port 5001", "Completed")
        ],
        "technologies": [
            "ReportLab 4.1.0, Pandas 2.1.4",
            "OpenPyXL 3.1.2",
            "Flask Jinja2 Templating"
        ],
        "learning_outcomes": [
            "Standardized programmatic document formatting using ReportLab flowables, tables, and page breaks.",
            "Integrated dual-Flask microservice instances sharing a common SQLite relational database."
        ],
        "challenges": "PDF layout text overflow when rendering student assessment details.",
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
        "period": "25-May-2026 to 30-May-2026",
        "tasks": [
            ("1", "Built Vite + React single-page application inside uai-counsellor-dashboard/", "Completed"),
            ("2", "Designed 11 dynamic views featuring TailwindCSS styling and Lucide icons", "Completed"),
            ("3", "Configured interactive Chart.js visualizations for subscale trend analysis", "Completed")
        ],
        "technologies": [
            "React 18, Vite 5",
            "TailwindCSS 3.4, Lucide-React",
            "Chart.js 4.4"
        ],
        "learning_outcomes": [
            "Engineered dynamic dashboard views using React state hooks (useState, useEffect).",
            "Applied responsive dark-theme design patterns using TailwindCSS utilities."
        ],
        "challenges": "Integrating client-side React routes into Flask server-rendered endpoints.",
        "solutions": "Compiled Vite static assets into Flask's static directory and rendered the root React <div id=\"root\"> via Jinja2 templates.",
        "plan_next_week": [
            ("1", "Inject Flask SQLite data directly into React global variables (window.__FLASK_KPIS__)", "4 Hours"),
            ("2", "Develop ProductivAI synthetic dataset generator (50,000 samples)", "4 Hours"),
            ("3", "Train and serialize Random Forest ML productivity regression model", "5 Hours")
        ]
    },
    {
        "week_title": "Fifth Week",
        "week_no": "Week 5",
        "period": "1-Jun-2026 to 6-Jun-2026",
        "tasks": [
            ("1", "Connected React frontend with Flask database using Jinja2 JSON script injection", "Completed"),
            ("2", "Built 50,000-sample synthetic lifestyle dataset generator (generate_dataset.py)", "Completed"),
            ("3", "Trained Random Forest Regressor and exported model via Joblib (productivity_model.pkl)", "Completed")
        ],
        "technologies": [
            "Scikit-Learn 1.3, Joblib",
            "NumPy, Pandas",
            "FastAPI, Uvicorn"
        ],
        "learning_outcomes": [
            "Evaluated regression models using metrics such as R², MAE, and MSE.",
            "Deserialized trained .pkl estimators inside FastAPI endpoints for real-time inference."
        ],
        "challenges": "Model inference latency spikes when serving REST requests under heavy load.",
        "solutions": "Cached the deserialized Joblib model instance in global application memory upon FastAPI startup.",
        "plan_next_week": [
            ("1", "Develop ProductivAI React frontend featuring score dials and Recharts", "5 Hours"),
            ("2", "Write integrated multi-process launcher scripts (launch_all.bat / .ps1)", "4 Hours"),
            ("3", "Perform end-to-end system testing, bug fixing, and documentation writing", "4 Hours")
        ]
    },
    {
        "week_title": "Sixth Week",
        "week_no": "Week 6",
        "period": "8-Jun-2026 to 13-Jun-2026",
        "tasks": [
            ("1", "Built ProductivAI React analytics dashboard with score dials and dark/light themes", "Completed"),
            ("2", "Created unified multi-process orchestrators (launch_all.bat and launch_all.ps1)", "Completed"),
            ("3", "Executed full system integration verification across ports 5000, 5001, and 8000", "Completed")
        ],
        "technologies": [
            "Windows Batch Scripting, PowerShell",
            "React 18, Recharts 2.10",
            "Framer Motion"
        ],
        "learning_outcomes": [
            "Automated multi-process application deployment using shell scripting techniques.",
            "Verified cross-origin data flows and API request validation across distinct microservices."
        ],
        "challenges": "Managing multiple terminal windows and port collisions during full-stack integration.",
        "solutions": "Wrote automated PowerShell start routines with explicit port bindings (-port 5000, -port 5001, -port 8000).",
        "plan_next_week": [
            ("1", "Final project deliverable submission and demonstration to faculty mentors", "0 Hours")
        ]
    }
]

TECH_STACK_TABLE_DATA = [
    ("Backend Core", "Python", "3.13.2", "Core runtime for web services, scoring engines, and ML models"),
    ("Web Framework", "Flask", "3.0.0", "REST routing, blueprint registration, Jinja2 template rendering"),
    ("API Server", "FastAPI", "0.109.0+", "Asynchronous REST backend serving ML predictions in ProductivAI"),
    ("WSGI Server", "Uvicorn / Gunicorn", "21.2.0", "Production HTTP server execution and process worker control"),
    ("ORM & Database", "Flask-SQLAlchemy", "3.1.1", "Relational database mapping for Users, Profiles, Scores, and Flags"),
    ("Database Engines", "SQLite / PostgreSQL", "3.x / 15.x", "Persistence engines for development (dev-db.sqlite) and production"),
    ("Migrations", "Flask-Migrate", "4.0.5", "Alembic-backed database schema migration wrapper"),
    ("Authentication", "Flask-Login / Flask-Bcrypt", "0.6.3 / 1.0.1", "Password hashing (bcrypt) and session cookie management"),
    ("Form Security", "Flask-WTF", "1.2.1", "Cross-Site Request Forgery (CSRF) token generation and validation"),
    ("Machine Learning", "Scikit-Learn", "1.3.2", "Regression pipelines (RandomForestRegressor, LinearRegression)"),
    ("Model Serialization", "Joblib", "1.3.2", "Binary serialization of trained ML estimator files (.pkl)"),
    ("Data Processing", "Pandas / NumPy", "2.1.4 / 1.26.2", "Dataframe manipulations, matrix calculations, and Excel exports"),
    ("PDF Generation", "ReportLab", "4.1.0", "Programmatic PDF layout building (SimpleDocTemplate, TableStyle)"),
    ("Excel Export", "OpenPyXL", "3.1.2", "Formatted Excel workbook rendering (.xlsx)"),
    ("Frontend Framework", "React", "18.2.0", "Single Page Application component tree rendering"),
    ("Build Tooling", "Vite", "5.0.8", "Frontend bundling, hot module reloading, and static compilation"),
    ("Styling & Icons", "TailwindCSS / Lucide-React", "3.4.1 / 0.300", "Responsive utility styling and vector iconography"),
    ("Data Visualization", "Chart.js / Recharts", "4.4.1 / 2.10.3", "Interactive dashboard analytics (radar, donut, and bar charts)"),
    ("Desktop Interface", "Tkinter", "Built-in", "GUI framework for offline desktop screening client (UAI_Quiz_App)")
]

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

def set_table_borders(table, color="B0B7C3", sz="4", val="single"):
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
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
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
    """Adds a single week report adhering exactly to the official university template."""
    if not is_first:
        doc.add_page_break()

    # Heading 1
    h1 = doc.add_paragraph()
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(4)
    h1.paragraph_format.space_after = Pt(10)
    r = h1.add_run("Summer Internship Weekly Report")
    r.font.name = "Times New Roman"
    r.font.size = Pt(18)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    # Student Details Heading
    p_sd = doc.add_paragraph()
    p_sd.paragraph_format.space_before = Pt(6)
    p_sd.paragraph_format.space_after = Pt(4)
    r = p_sd.add_run("Student Details")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True

    # Student Details Table (3x2)
    tbl_sd = doc.add_table(rows=3, cols=2)
    tbl_sd.style = "Table Grid"
    set_table_borders(tbl_sd)
    col_widths = [Inches(3.0), Inches(3.0)]
    for row in tbl_sd.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    format_cell(tbl_sd.rows[0].cells[0], "Student Name: ", "Himanshu Pathak")
    format_cell(tbl_sd.rows[0].cells[1], "Roll No.: ", "UAI05BT12417")
    format_cell(tbl_sd.rows[1].cells[0], "Year/ Semester: ", "2nd Year / 4th Semester")
    format_cell(tbl_sd.rows[1].cells[1], "Email Id: ", "himanshu.pathak@universalai.in")
    format_cell(tbl_sd.rows[2].cells[0], "Faculty Mentor : ", "Prof. Rajesh Bhise")
    format_cell(tbl_sd.rows[2].cells[1], "Department: ", "School of Ai & Future Technologies")

    # Company Details Heading
    p_cd = doc.add_paragraph()
    p_cd.paragraph_format.space_before = Pt(8)
    p_cd.paragraph_format.space_after = Pt(4)
    r = p_cd.add_run("Company Details:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True

    # Company Details Table (3x2)
    tbl_cd = doc.add_table(rows=3, cols=2)
    tbl_cd.style = "Table Grid"
    set_table_borders(tbl_cd)
    for row in tbl_cd.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    format_cell(tbl_cd.rows[0].cells[0], "Company Name: ", "Ai Cell, Universal Ai University")
    format_cell(tbl_cd.rows[0].cells[1], "Department Name: ", "School of Ai & Future Technologies")
    format_cell(tbl_cd.rows[1].cells[0], "Company Manger Name: ", "Prof. Rajesh Bhise / Dr. Shivaji Pawar")
    format_cell(tbl_cd.rows[1].cells[1], "Official Mail Id: ", "")
    format_cell(tbl_cd.rows[2].cells[0], "Contact No: ", "")
    format_cell(tbl_cd.rows[2].cells[1], "", "")

    # Meta Paragraphs (Project Title, Week No, Reporting Period)
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(8)
    p_meta.paragraph_format.space_after = Pt(2)
    p_meta.paragraph_format.line_spacing = 1.25

    r = p_meta.add_run("Project Title: ")
    r.bold = True
    r.font.name = "Times New Roman"
    r = p_meta.add_run("UAi PsychePortal & AI Productivity Analyzer Suite\n")
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
    p_h.paragraph_format.space_before = Pt(8)
    p_h.paragraph_format.space_after = Pt(4)
    r = p_h.add_run("1. Weekly Task")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

    # Task Table
    tasks = data["tasks"]
    tbl_task = doc.add_table(rows=1 + len(tasks), cols=3)
    tbl_task.style = "Table Grid"
    set_table_borders(tbl_task)
    task_widths = [Inches(0.8), Inches(4.2), Inches(1.0)]

    # Header Row
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
    p_h.paragraph_format.space_before = Pt(8)
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

    # 3. Learning Outcomes
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(8)
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
    p_h.paragraph_format.space_before = Pt(8)
    p_h.paragraph_format.space_after = Pt(2)
    r = p_h.add_run("4. Challenges Faced & Solutions")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

    p_cs = doc.add_paragraph()
    p_cs.paragraph_format.space_before = Pt(2)
    p_cs.paragraph_format.space_after = Pt(4)
    p_cs.paragraph_format.line_spacing = 1.2

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
    p_h.paragraph_format.space_before = Pt(8)
    p_h.paragraph_format.space_after = Pt(4)
    r = p_h.add_run("5. Plan for Next Week")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

    # Plan Table
    plans = data["plan_next_week"]
    tbl_plan = doc.add_table(rows=1 + len(plans), cols=3)
    tbl_plan.style = "Table Grid"
    set_table_borders(tbl_plan)
    plan_widths = [Inches(0.8), Inches(4.2), Inches(1.0)]

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

    # Student Signature
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(12)
    p_sig.paragraph_format.space_after = Pt(8)
    r = p_sig.add_run("Student Signature: ")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r = p_sig.add_run("Himanshu Pathak (Digital Signature - Verified)")
    r.bold = False
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

print("build_weekly_report_section defined successfully.")
