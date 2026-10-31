import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import docx2pdf
import shutil
import os

TEMPLATE_PATH = r"C:\Users\Himanshu Pathak\Downloads\Summer_Internship_Weekly_Report (1).docx"

OUTPUT_DOCX = r"d:\AI INTERNSHIP\HimanshuPathak_SIP_WeeklyReport.docx"
OUTPUT_PDF = r"d:\AI INTERNSHIP\HimanshuPathak_SIP_WeeklyReport.pdf"

DOWNLOADS_DOCX = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_SIP_WeeklyReport.docx"
DOWNLOADS_PDF = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_SIP_WeeklyReport.pdf"

MASTER_DOCX = r"d:\AI INTERNSHIP\Universal_Ai_University_Internship_Report_and_Weekly_Reports.docx"
MASTER_PDF = r"d:\AI INTERNSHIP\HimanshuPathak_Universal_Ai_University_Complete_Internship_Report.pdf"
DOWNLOADS_MASTER_PDF = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_Universal_Ai_University_Complete_Internship_Report.pdf"

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

def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
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

def format_cell_text(cell, text, bold=True, font_size=11, font_name="Times New Roman", align=WD_ALIGN_PARAGRAPH.LEFT):
    set_cell_margins(cell, top=40, bottom=40, left=80, right=80)
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(text)
    r.font.name = font_name
    r.font.size = Pt(font_size)
    r.bold = bold
    r.font.color.rgb = RGBColor(0, 0, 0)

def add_week_to_doc(doc, data, is_first=False):
    """Adds a weekly report matching Sandesh Halmadge's reference formatting exactly."""
    if not is_first:
        doc.add_page_break()

    # Heading 1: Summer Internship Weekly Report
    h1 = doc.add_paragraph()
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(0)
    h1.paragraph_format.space_after = Pt(6)
    r = h1.add_run("Summer Internship Weekly Report")
    r.font.name = "Times New Roman"
    r.font.size = Pt(18)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    # Student Details
    p_sd = doc.add_paragraph()
    p_sd.paragraph_format.space_before = Pt(4)
    p_sd.paragraph_format.space_after = Pt(2)
    r = p_sd.add_run("Student Details")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True

    # Student Details Table (3 rows x 2 cols)
    tbl_sd = doc.add_table(rows=3, cols=2)
    tbl_sd.style = "Table Grid"
    set_table_borders(tbl_sd)
    col_w = [Inches(3.0), Inches(3.0)]
    for row in tbl_sd.rows:
        for idx, w in enumerate(col_w):
            row.cells[idx].width = w

    format_cell_text(tbl_sd.rows[0].cells[0], "Student Name: Himanshu Pathak", bold=True)
    format_cell_text(tbl_sd.rows[0].cells[1], "Roll No.: UAI05BT12417", bold=True)
    format_cell_text(tbl_sd.rows[1].cells[0], "Year/ Semester: 2nd Year / 4th Semester", bold=True)
    format_cell_text(tbl_sd.rows[1].cells[1], "Email Id: himanshu.pathak@universalai.in", bold=True)
    format_cell_text(tbl_sd.rows[2].cells[0], "Faculty Mentor : Prof. Rajesh Bhise", bold=True)
    format_cell_text(tbl_sd.rows[2].cells[1], "", bold=True)

    # Company Details:
    p_cd = doc.add_paragraph()
    p_cd.paragraph_format.space_before = Pt(6)
    p_cd.paragraph_format.space_after = Pt(2)
    r = p_cd.add_run("Company Details:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True

    # Company Details Table (3 rows x 2 cols)
    tbl_cd = doc.add_table(rows=3, cols=2)
    tbl_cd.style = "Table Grid"
    set_table_borders(tbl_cd)
    for row in tbl_cd.rows:
        for idx, w in enumerate(col_w):
            row.cells[idx].width = w

    format_cell_text(tbl_cd.rows[0].cells[0], "Company Name: Ai Cell, Universal Ai University", bold=True)
    format_cell_text(tbl_cd.rows[0].cells[1], "Department Name: School of Ai & Future Technologies", bold=True)
    format_cell_text(tbl_cd.rows[1].cells[0], "Company Manger Name:  Prof. Rajesh Bhise / Dr. Shivaji Pawar", bold=True)
    format_cell_text(tbl_cd.rows[1].cells[1], "Official Mail Id:", bold=True)
    format_cell_text(tbl_cd.rows[2].cells[0], "Contact No:", bold=True)
    format_cell_text(tbl_cd.rows[2].cells[1], "", bold=True)

    # Metadata lines (bold Times New Roman 11pt)
    p_meta1 = doc.add_paragraph()
    p_meta1.paragraph_format.space_before = Pt(6)
    p_meta1.paragraph_format.space_after = Pt(1)
    r = p_meta1.add_run("Project Title: UAi PsychePortal & AI Productivity Analyzer Suite")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True

    p_meta2 = doc.add_paragraph()
    p_meta2.paragraph_format.space_before = Pt(1)
    p_meta2.paragraph_format.space_after = Pt(1)
    r = p_meta2.add_run(f"Week No.: {data['week_title']}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True

    p_meta3 = doc.add_paragraph()
    p_meta3.paragraph_format.space_before = Pt(1)
    p_meta3.paragraph_format.space_after = Pt(4)
    r = p_meta3.add_run(f"Reporting Period: {data['period']}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True

    # 1. Weekly Task
    p_h1 = doc.add_paragraph()
    p_h1.paragraph_format.space_before = Pt(4)
    p_h1.paragraph_format.space_after = Pt(2)
    r = p_h1.add_run("1. Weekly Task")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True

    # Weekly Task Table (Table 2)
    tasks = data["tasks"]
    tbl_task = doc.add_table(rows=1 + len(tasks), cols=3)
    tbl_task.style = "Table Grid"
    set_table_borders(tbl_task)
    task_w = [Inches(0.8), Inches(4.2), Inches(1.0)]

    for idx, w in enumerate(task_w):
        tbl_task.rows[0].cells[idx].width = w
    format_cell_text(tbl_task.rows[0].cells[0], "S. No", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell_text(tbl_task.rows[0].cells[1], "Task Description", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell_text(tbl_task.rows[0].cells[2], "Status", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    for r_idx, (sno, desc, status) in enumerate(tasks, start=1):
        for idx, w in enumerate(task_w):
            tbl_task.rows[r_idx].cells[idx].width = w
        format_cell_text(tbl_task.rows[r_idx].cells[0], sno, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell_text(tbl_task.rows[r_idx].cells[1], desc, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell_text(tbl_task.rows[r_idx].cells[2], status, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # 2. Technologies/Tools Used
    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(6)
    p_h2.paragraph_format.space_after = Pt(2)
    r = p_h2.add_run("2. Technologies/Tools Used")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True

    for tech in data["technologies"]:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(0)
        p_item.paragraph_format.space_after = Pt(1)
        p_item.paragraph_format.left_indent = Inches(0.25)
        r_b = p_item.add_run("  ")
        r_b.font.name = "Symbol"
        r_b.font.size = Pt(10)
        r_t = p_item.add_run(tech)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)
        r_t.bold = True

    # 3. Learning Outcomes
    p_h3 = doc.add_paragraph()
    p_h3.paragraph_format.space_before = Pt(6)
    p_h3.paragraph_format.space_after = Pt(2)
    r = p_h3.add_run("3. Learning Outcomes")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True

    for outcome in data["learning_outcomes"]:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(0)
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.left_indent = Inches(0.25)
        r_b = p_item.add_run("  ")
        r_b.font.name = "Symbol"
        r_b.font.size = Pt(10)
        r_t = p_item.add_run(outcome)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)
        r_t.bold = False

    # 4. Challenges Faced & Solutions
    p_h4 = doc.add_paragraph()
    p_h4.paragraph_format.space_before = Pt(6)
    p_h4.paragraph_format.space_after = Pt(2)
    r = p_h4.add_run("4. Challenges Faced & Solutions")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.5)
    r.bold = True

    p_chal = doc.add_paragraph()
    p_chal.paragraph_format.space_before = Pt(1)
    p_chal.paragraph_format.space_after = Pt(3)
    r_lbl = p_chal.add_run("Challenges: ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(11)
    r_lbl.bold = True
    r_txt = p_chal.add_run(data["challenges"])
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(11)
    r_txt.bold = False

    p_sol = doc.add_paragraph()
    p_sol.paragraph_format.space_before = Pt(1)
    p_sol.paragraph_format.space_after = Pt(4)
    r_lbl = p_sol.add_run("Solutions: ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(11)
    r_lbl.bold = True
    r_txt = p_sol.add_run(data["solutions"])
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(11)
    r_txt.bold = False

    # 5. Plan for Next Week
    p_h5 = doc.add_paragraph()
    p_h5.paragraph_format.space_before = Pt(6)
    p_h5.paragraph_format.space_after = Pt(2)
    r = p_h5.add_run("5. Plan for Next Week")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True

    # Plan Table (Table 3)
    plans = data["plan_next_week"]
    tbl_plan = doc.add_table(rows=1 + len(plans), cols=3)
    tbl_plan.style = "Table Grid"
    set_table_borders(tbl_plan)
    plan_w = [Inches(0.8), Inches(4.2), Inches(1.0)]

    for idx, w in enumerate(plan_w):
        tbl_plan.rows[0].cells[idx].width = w
    format_cell_text(tbl_plan.rows[0].cells[0], "S. No", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell_text(tbl_plan.rows[0].cells[1], "Task to be done", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell_text(tbl_plan.rows[0].cells[2], "Estimated Time", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    for r_idx, (sno, task_todo, est_time) in enumerate(plans, start=1):
        for idx, w in enumerate(plan_w):
            tbl_plan.rows[r_idx].cells[idx].width = w
        format_cell_text(tbl_plan.rows[r_idx].cells[0], sno, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell_text(tbl_plan.rows[r_idx].cells[1], task_todo, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT)
        format_cell_text(tbl_plan.rows[r_idx].cells[2], est_time, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # Signature Block (Prepared for physical signature)
    # 1. "X" and signature blank space
    p_x = doc.add_paragraph()
    p_x.paragraph_format.space_before = Pt(14)
    p_x.paragraph_format.space_after = Pt(0)
    p_x.paragraph_format.left_indent = Inches(0.1)
    
    r_x = p_x.add_run("X  ")
    r_x.font.name = "Arial"
    r_x.font.size = Pt(22)
    r_x.font.color.rgb = RGBColor(0, 0, 0)

    # 2. Student Name in Segoe UI 8.5pt with top line
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(2)
    p_name.paragraph_format.space_after = Pt(2)
    p_name.paragraph_format.left_indent = Inches(0.1)
    r_line = p_name.add_run("_________________________\nHimanshu Pathak")
    r_line.font.name = "Segoe UI"
    r_line.font.size = Pt(8.5)
    r_line.font.color.rgb = RGBColor(0, 0, 0)

    # 3. Student Signature
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(4)
    p_sig.paragraph_format.space_after = Pt(8)
    r_sig_lbl = p_sig.add_run("Student Signature:")
    r_sig_lbl.font.name = "Times New Roman"
    r_sig_lbl.font.size = Pt(11)
    r_sig_lbl.bold = True
    r_sig_lbl.font.color.rgb = RGBColor(0, 0, 0)

def main():
    print("Loading university template docx...")
    doc = docx.Document(TEMPLATE_PATH)

    # Clear initial template body elements except the last sectPr
    body = doc._element.body
    for child in list(body)[:-1]:
        body.remove(child)

    print("Populating all 6 weekly reports for Himanshu Pathak...")
    for idx, data in enumerate(WEEKLY_DATA):
        print(f"  Adding {data['week_title']} ({data['week_no']})...")
        add_week_to_doc(doc, data, is_first=(idx == 0))

    print(f"Saving Word document: {OUTPUT_DOCX}...")
    doc.save(OUTPUT_DOCX)
    shutil.copy(OUTPUT_DOCX, DOWNLOADS_DOCX)

    print("Converting Word document to PDF using Microsoft Word engine...")
    docx2pdf.convert(OUTPUT_DOCX, OUTPUT_PDF)
    shutil.copy(OUTPUT_PDF, DOWNLOADS_PDF)
    print(f"PDF successfully created at:\n1. {OUTPUT_PDF}\n2. {DOWNLOADS_PDF}")

    if os.path.exists(MASTER_DOCX):
        print("Converting Comprehensive Master Report to PDF...")
        docx2pdf.convert(MASTER_DOCX, MASTER_PDF)
        shutil.copy(MASTER_PDF, DOWNLOADS_MASTER_PDF)
        print(f"Master PDF created at:\n1. {MASTER_PDF}\n2. {DOWNLOADS_MASTER_PDF}")

    print("All tasks completed successfully!")

if __name__ == "__main__":
    main()
