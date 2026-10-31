import re

# Read current builder script
with open("build_exact_university_sip_handbook.py", "r", encoding="utf-8") as f:
    content = f.read()

# Verify where Section 2 starts
sec2_marker = '    # SECTION 2: SUMMER INTERNSHIP WEEKLY REPORTS (PAGES 31 TO 43)\n    # -----------------------------------------------------------------------\n    print("Configuring Section 2: Weekly Reports (Pages 31 to 43)...")'
assert sec2_marker in content, "Section 2 marker not found"

part1 = content[:content.find(sec2_marker)]

# New Section 2 implementation
new_sec2 = '''    # SECTION 2: SUMMER INTERNSHIP WEEKLY REPORTS (PAGES 31 TO 43)
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
        "Enabled FastAPI CORSMiddleware with granular allowed origins allow_origins=[\"http://localhost:5000\"]."
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
    p_sig_mid.paragraph_format.space_before = Pt(40)
    p_sig_mid.paragraph_format.space_after = Pt(4)
    r_sm = p_sig_mid.add_run(
        "Student Signature: (Digital Signature)\n\n"
        "_________________________\n"
        "Himanshu Pathak\n"
        "Roll No.: UAI05BT12417\n\n\n"
        "Faculty Mentor Signature: _________________________\n"
        "Prof. Rajesh Bhise\n"
        "School of AI & Future Technologies"
    )
    r_sm.font.name = "Times New Roman"
    r_sm.font.size = Pt(11)
    r_sm.bold = True
    r_sm.font.color.rgb = COLOR_BLACK
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
    add_weekly_meta(doc, "8th week", "22 June 2026 - 04 July 2026")
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
    p_sig_final.paragraph_format.space_before = Pt(28)
    p_sig_final.paragraph_format.space_after = Pt(4)
    r_sf = p_sig_final.add_run(
        "Student Signature: (Digital Signature)\\n\\n"
        "_________________________\\n"
        "Himanshu Pathak\\n"
        "Roll No.: UAI05BT12417\\n\\n"
        "Faculty Mentor Signature: _________________________\\n"
        "Prof. Rajesh Bhise\\n"
        "School of AI & Future Technologies"
    )
    r_sf.font.name = "Times New Roman"
    r_sf.font.size = Pt(11)
    r_sf.bold = True
    r_sf.font.color.rgb = COLOR_BLACK

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
'''

# Also add the new helper functions before main() in part1
helper_functions = '''
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
    format_cell(tbl_cd.rows[1].cells[1], "Official Mail Id:\\naicell@universalai.in", bold=True, font_name="Times New Roman", font_size=10.5)
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
    r = p.add_run(f"Week No.: {week_str}\\nReporting Period: {period_str}")
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
'''

# Insert helper functions before def main():
main_idx = part1.find("def main():")
part1_with_helpers = part1[:main_idx] + helper_functions + "\n" + part1[main_idx:]

final_code = part1_with_helpers + new_sec2

with open("build_exact_university_sip_handbook.py", "w", encoding="utf-8") as f:
    f.write(final_code)

print("Updated build_exact_university_sip_handbook.py successfully.")
