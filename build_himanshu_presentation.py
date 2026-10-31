import os
import shutil
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

SRC_PPT = r"C:\Users\Himanshu Pathak\Downloads\FlowCore_Digital_SIP_Presentation.pptx"
OUT_WORKSPACE = r"d:\AI INTERNSHIP\HimanshuPathak_UAI05BT12417_SIP_Presentation_12Slides.pptx"
OUT_DOWNLOADS = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_UAI05BT12417_SIP_Presentation_12Slides.pptx"

LOGO_IMG = r"d:\AI INTERNSHIP\scratch\master_logo.png"
FIG1_1 = r"d:\AI INTERNSHIP\report_figures\fig1_1_methodology_flow.png"
FIG1_2 = r"d:\AI INTERNSHIP\report_figures\fig1_2_er_diagram.png"
FIG1_3 = r"d:\AI INTERNSHIP\report_figures\fig1_3_state_machine.png"
FIG_BENCHMARK = r"d:\AI INTERNSHIP\report_figures\fig_results_benchmark.png"

# Color constants matching FlowCore / University theme
COLOR_NAVY = RGBColor(0x0F, 0x17, 0x2A)
COLOR_BLUE = RGBColor(0x1E, 0x3A, 0x8A)
COLOR_MUTED = RGBColor(0x47, 0x55, 0x69)
COLOR_SLATE = RGBColor(0x33, 0x41, 0x55)
COLOR_RED = RGBColor(0xEF, 0x44, 0x44)
COLOR_GREEN = RGBColor(0x65, 0xA3, 0x0D)

def set_text(shape, text, font_name="Times New Roman", font_size_pt=None, bold=None, color_rgb=None, align=None):
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    tf.word_wrap = True
    
    # Store existing font properties if not provided
    if len(tf.paragraphs) > 0 and len(tf.paragraphs[0].runs) > 0:
        r0 = tf.paragraphs[0].runs[0]
        if font_size_pt is None and r0.font.size:
            font_size_pt = r0.font.size.pt
        if bold is None:
            bold = r0.font.bold
        if color_rgb is None and r0.font.color and r0.font.color.type == pptx.enum.dml.MSO_COLOR_TYPE.RGB:
            color_rgb = r0.font.color.rgb

    tf.clear()
    p = tf.paragraphs[0]
    if align:
        p.alignment = align
    
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    if font_size_pt:
        run.font.size = Pt(font_size_pt)
    if bold is not None:
        run.font.bold = bold
    if color_rgb:
        run.font.color.rgb = color_rgb

def replace_picture(slide, old_shape, new_img_path, target_left=None, target_top=None, target_width=None, target_height=None):
    l = target_left if target_left is not None else old_shape.left
    t = target_top if target_top is not None else old_shape.top
    w = target_width if target_width is not None else old_shape.width
    h = target_height if target_height is not None else old_shape.height
    
    sp = old_shape._element
    sp.getparent().remove(sp)
    
    new_pic = slide.shapes.add_picture(new_img_path, l, t, w, h)
    return new_pic

def build_presentation():
    prs = pptx.Presentation(SRC_PPT)
    
    # -------------------------------------------------------------
    # SLIDE 1: Cover Page
    # -------------------------------------------------------------
    s1 = prs.slides[0]
    for shape in s1.shapes:
        name = shape.name
        if name == "TextBox 20":
            set_text(shape, "Himanshu Pathak", font_size_pt=16.5, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 22":
            set_text(shape, "UID: UAI05BT12417", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 26":
            set_text(shape, "Full-Stack AI & Clinical Assessment Systems Intern", font_size_pt=13.5, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 30":
            set_text(shape, "AI Cell, Universal AI University", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 32":
            set_text(shape, "4th May 2026 - 13th June 2026", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 36":
            set_text(shape, "Faculty Guide: Prof. Rajesh Bhise", font_size_pt=13.5, bold=True, color_rgb=COLOR_MUTED)
        elif name == "TextBox 38":
            set_text(shape, "Head of Department: Dr. Shivaji Pawar", font_size_pt=13.5, bold=True, color_rgb=COLOR_MUTED)
        elif name == "TextBox 40":
            set_text(shape, "Full-Stack AI & Clinical Assessment Systems:\nEngineering the UAi PsychePortal Suite & ProductivAI", font_size_pt=23.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 41":
            set_text(shape, "Batch: 2024-28", font_size_pt=12.5, bold=False, color_rgb=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 2: Company / Organization Overview
    # -------------------------------------------------------------
    s2 = prs.slides[1]
    # Replace Growisto logo with Universal AI University logo
    pic_s2 = [s for s in s2.shapes if "PICTURE" in str(s.shape_type)]
    if pic_s2 and os.path.exists(LOGO_IMG):
        replace_picture(s2, pic_s2[0], LOGO_IMG, target_left=Inches(8.75), target_top=Inches(2.75), target_width=Inches(2.6), target_height=Inches(0.64))
        
    for shape in s2.shapes:
        name = shape.name
        if name == "TextBox 72":
            set_text(shape, "AI Cell, Universal AI University", font_size_pt=20.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 78":
            set_text(shape, "Established under Maharashtra Act No. III of 2023; recognized by UGC.", font_size_pt=14.0, bold=False, color_rgb=COLOR_SLATE)
        elif name == "TextBox 82":
            set_text(shape, "India's 1st AI University dedicated to cutting-edge AI, ML, and future technologies.", font_size_pt=14.0, bold=False, color_rgb=COLOR_SLATE)
        elif name == "TextBox 86":
            set_text(shape, "Interdisciplinary engineering hub bridging clinical psychometrics, ML, and scalable software.", font_size_pt=14.0, bold=False, color_rgb=COLOR_SLATE)
        elif name == "TextBox 74":
            set_text(shape, "School of AI & Future Technologies", font_size_pt=20.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 90":
            set_text(shape, "Develops production software for campus operations, student health, and lifestyle tracking.", font_size_pt=14.0, bold=False, color_rgb=COLOR_SLATE)
        elif name == "TextBox 94":
            set_text(shape, "Engineers end-to-end data pipelines, standardized diagnostic tools, and predictive ML systems.", font_size_pt=14.0, bold=False, color_rgb=COLOR_SLATE)
        elif name == "TextBox 70":
            set_text(shape, "Transforming institutional student wellness and productivity through automated clinical intelligence and predictive AI.", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)

    # -------------------------------------------------------------
    # SLIDE 3: Internship Objectives
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    for shape in s3.shapes:
        name = shape.name
        if name == "TextBox 21":
            set_text(shape, "Standardized Clinical Ingestion", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 23":
            set_text(shape, "Build a zero-friction, mobile-responsive web portal (Port 5001) for standardized psychometric assessments (DASS-21, BFI-44, EQ/SQ).", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 25":
            set_text(shape, "Real-Time Risk State Machine", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 27":
            set_text(shape, "Implement exact mathematical reverse scoring (6 - R) and real-time crisis event triggers alerting counsellors to severe distress.", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 33":
            set_text(shape, "Predictive Lifestyle Analytics", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 29":
            set_text(shape, "Train and deploy Scikit-Learn regression pipelines (ProductivAI) to predict daily productivity and provide actionable habit interventions.", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 4: Roles & Responsibilities
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    for shape in s4.shapes:
        name = shape.name
        if name == "TextBox 85":
            set_text(shape, "Backend Architecture & Data Modeling", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 87":
            set_text(shape, "Designed normalized relational schemas in SQLAlchemy ORM for Users, Profiles, Scores, and RiskAlerts across SQLite (WAL) and PostgreSQL.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 89":
            set_text(shape, "Clinical Scoring & Crisis Alert Pipeline", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 91":
            set_text(shape, "Implemented DASS-21, BFI-44 (6 - R reverse keying), and automated server-side triggers for immediate counsellor crisis triage.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 93":
            set_text(shape, "SPA Frontend & ReportLab PDF Engine", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 95":
            set_text(shape, "Built 11 React SPA dashboard views in Vite + TailwindCSS, and programmed dynamic ReportLab multi-page clinical diagnostic PDF generators.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 97":
            set_text(shape, "Machine Learning & System Orchestration", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 99":
            set_text(shape, "Trained Random Forest models (R^2 = 0.912) on 50k samples served via FastAPI (Port 8000), and automated multi-process deployment scripts.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 5: Project Overview
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    for shape in s5.shapes:
        name = shape.name
        if name == "TextBox 21":
            set_text(shape, "Dual-service ecosystem unifying clinical psychological assessment with machine learning lifestyle analytics.", font_size_pt=15.0, bold=False, color_rgb=COLOR_NAVY)
        elif name == "TextBox 36":
            set_text(shape, "\"Higher education institutions suffer from 3-14 day delays and error-prone manual reverse scoring in student mental health screening, with zero empirical correlation to daily lifestyle habits.\"", font_size_pt=14.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 25":
            set_text(shape, "Zero-Friction Ingestion: Mobile-responsive standalone web intake running on Port 5001.", font_size_pt=15.0, bold=True, color_rgb=COLOR_SLATE)
        elif name == "TextBox 27":
            set_text(shape, "Automated Scoring & Risk Engine: Exact DASS-21, BFI-44 (6 - R), and instant crisis flags.", font_size_pt=15.0, bold=True, color_rgb=COLOR_SLATE)
        elif name == "TextBox 29":
            set_text(shape, "Programmatic Clinical PDF Dossiers: Dynamic ReportLab rendering generated in under 850ms.", font_size_pt=15.0, bold=True, color_rgb=COLOR_SLATE)
        elif name == "TextBox 31":
            set_text(shape, "ProductivAI ML Analytics: FastAPI engine predicting productivity from sleep, study, and mood.", font_size_pt=15.0, bold=True, color_rgb=COLOR_SLATE)

    # -------------------------------------------------------------
    # SLIDE 6: Technologies & Tools Used
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    for shape in s6.shapes:
        name = shape.name
        if name == "TextBox 30":
            set_text(shape, "Frontend / Interface", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 32":
            set_text(shape, "React 18, Vite 5, TailwindCSS 3.4, Chart.js 4.4, Lucide", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 34":
            set_text(shape, "Core Backend", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 36":
            set_text(shape, "Python 3.13, Flask 3.0.0 (App Factory), FastAPI 0.109+", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 38":
            set_text(shape, "Database & Storage", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 40":
            set_text(shape, "Flask-SQLAlchemy, SQLite (WAL Mode), PostgreSQL 15", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 42":
            set_text(shape, "AI / Machine Learning", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 44":
            set_text(shape, "Scikit-Learn (Random Forest), Pandas, NumPy, Joblib", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 46":
            set_text(shape, "Authentication & Security", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 48":
            set_text(shape, "Flask-Login, Flask-Bcrypt, Flask-WTF (CSRF), Cookies", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 50":
            set_text(shape, "Reporting & Orchestration", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 52":
            set_text(shape, "ReportLab 4.1 (PDF), OpenPyXL, PowerShell / Batch", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 7: Methodology & Workflow
    # -------------------------------------------------------------
    s7 = prs.slides[6]
    pic_s7 = [s for s in s7.shapes if "PICTURE" in str(s.shape_type)]
    if pic_s7 and os.path.exists(FIG1_1):
        replace_picture(s7, pic_s7[0], FIG1_1, target_left=Inches(6.8), target_top=Inches(2.2), target_width=Inches(5.8), target_height=Inches(3.4))
        
    for shape in s7.shapes:
        name = shape.name
        if name == "TextBox 11":
            set_text(shape, "Phase 1: Requirements & Domain Analysis", font_size_pt=15.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 13":
            set_text(shape, "Analyzed Lovibond DASS-21 and John & Srivastava BFI-44 clinical norms; mapped scoring formulations.", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 15":
            set_text(shape, "Phase 2: Relational Architecture & Modeling", font_size_pt=15.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 17":
            set_text(shape, "Designed 3NF database schema, decoupled microservices, and established RESTful API contracts.", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 19":
            set_text(shape, "Phase 3: Core Implementation & ML Training", font_size_pt=15.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 21":
            set_text(shape, "Built app/scoring.py, ReportLab PDF generators, and trained Random Forest on 50k lifestyle rows.", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 23":
            set_text(shape, "Phase 4: Integration, Testing & Deployment", font_size_pt=15.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 25":
            set_text(shape, "Developed React SPA, executed unit/integration tests, and authored launch_all orchestrators.", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 8: System Architecture & Data Model
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    for shape in s8.shapes:
        name = shape.name
        if name == "TextBox 32":
            set_text(shape, "Multi-service relational architecture with automated lead triage and clinical risk state machines.", font_size_pt=14.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 35":
            set_text(shape, "Entity-Relationship Model (SQLAlchemy ORM)", font_size_pt=13.5, bold=True, color_rgb=COLOR_MUTED)
        elif name == "TextBox 36":
            set_text(shape, "Clinical Scoring & Risk State Machine", font_size_pt=13.5, bold=True, color_rgb=COLOR_MUTED)

    pic_s8 = [s for s in s8.shapes if "PICTURE" in str(s.shape_type)]
    if len(pic_s8) >= 2:
        replace_picture(s8, pic_s8[0], FIG1_2, target_left=Inches(1.0), target_top=Inches(2.35), target_width=Inches(5.4), target_height=Inches(3.35))
        replace_picture(s8, pic_s8[1], FIG1_3, target_left=Inches(6.8), target_top=Inches(2.35), target_width=Inches(5.5), target_height=Inches(3.35))

    # -------------------------------------------------------------
    # SLIDE 9: Key Contributions & Achievements
    # -------------------------------------------------------------
    s9 = prs.slides[8]
    for shape in s9.shapes:
        name = shape.name
        if name == "TextBox 5":
            set_text(shape, "Dual-Service Production Ecosystem", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 6":
            set_text(shape, "Architected, developed, and deployed UAi PsychePortal (Ports 5000/5001) and ProductivAI ML engine (Port 8000).", font_size_pt=12.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 8":
            set_text(shape, "Zero Crisis Window Latency", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 9":
            set_text(shape, "Eliminated 3-14 day manual triage delays by triggering automated emergency risk alerts in under 28ms.", font_size_pt=12.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 11":
            set_text(shape, "100% Algorithmic Scoring Fidelity", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 12":
            set_text(shape, "Implemented flawless DASS-21 subscale math and BFI-44 6-R reverse scoring with 100% test coverage.", font_size_pt=12.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 14":
            set_text(shape, "Automated Clinical Dossier Generation", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 15":
            set_text(shape, "Built dynamic ReportLab PDF generator compiling multi-page diagnostic records in under 850ms, saving 40 min/student.", font_size_pt=12.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 17":
            set_text(shape, "High-Precision ML Productivity Model", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 18":
            set_text(shape, "Trained Random Forest Regressor achieving R^2 = 0.912 and MAE = 3.42, served via FastAPI with sub-15ms inference.", font_size_pt=12.5, bold=False, color_rgb=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 10: Challenges & Solutions
    # -------------------------------------------------------------
    s10 = prs.slides[9]
    for shape in s10.shapes:
        name = shape.name
        if name == "TextBox 15":
            set_text(shape, "Cyclic Imports & Modular Decoupling", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 17":
            set_text(shape, "Tight coupling between SQLAlchemy models, auth blueprints, and route handlers causing circular imports.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 19":
            set_text(shape, "Reverse Keying & Missing Item Failures", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 21":
            set_text(shape, "Missing survey inputs or manual inversions crashing matrix subscale calculations.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 23":
            set_text(shape, "Multi-Service Port Orchestration", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 25":
            set_text(shape, "Managing concurrent terminal execution and port collisions across ports 5000, 5001, and 8000.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 27":
            set_text(shape, "Implemented Flask Application Factory pattern (create_app), cleanly isolating model definitions from blueprint routes.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 29":
            set_text(shape, "Engineered safe dictionary lookups with neutral default imputation (3 for BFI, 0 for DASS) and automated 6 - R transforms.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 31":
            set_text(shape, "Authored unified PowerShell & Batch scripts (launch_all.bat) with automated port-binding and health checks.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 11: Results & Impact
    # -------------------------------------------------------------
    s11 = prs.slides[10]
    for shape in s11.shapes:
        name = shape.name
        if name == "TextBox 32":
            set_text(shape, "Sub-15ms ML inference, 12ms clinical scoring, and 850ms dynamic PDF dossier generation.", font_size_pt=14.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 37":
            set_text(shape, "Reduced institutional crisis identification time from 14 days to real time, saving counsellors 40 minutes per evaluation.", font_size_pt=14.0, bold=False, color_rgb=COLOR_MUTED)

    pic_s11 = [s for s in s11.shapes if "PICTURE" in str(s.shape_type)]
    if pic_s11 and os.path.exists(FIG_BENCHMARK):
        replace_picture(s11, pic_s11[0], FIG_BENCHMARK, target_left=Inches(1.85), target_top=Inches(2.72), target_width=Inches(9.1), target_height=Inches(3.52))

    # -------------------------------------------------------------
    # SLIDE 12: Future Scope & Recommendations
    # -------------------------------------------------------------
    s12 = prs.slides[11]
    for shape in s12.shapes:
        name = shape.name
        if name == "TextBox 85":
            set_text(shape, "Cloud-Native Containerization", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 87":
            set_text(shape, "Containerize Flask, FastAPI, and React services with Docker and Kubernetes for high-availability multi-campus deployment.", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 89":
            set_text(shape, "Cross-Platform Mobile Application", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 91":
            set_text(shape, "Develop a native Flutter mobile client for Android/iOS to facilitate daily lifestyle tracking and push notifications.", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 93":
            set_text(shape, "Generative LLM Clinical Summaries", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 95":
            set_text(shape, "Integrate local, HIPAA-compliant LLMs to synthesize longitudinal assessment histories into draft counsellor consultation notes.", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 97":
            set_text(shape, "Continuous ML Model Retraining", font_size_pt=17.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 99":
            set_text(shape, "Implement automated MLOps pipelines to continuously retrain the Random Forest model on verified student academic outcomes.", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)

    # Save to workspace and downloads
    prs.save(OUT_WORKSPACE)
    shutil.copyfile(OUT_WORKSPACE, OUT_DOWNLOADS)
    print(f"Successfully generated:\n1. {OUT_WORKSPACE}\n2. {OUT_DOWNLOADS}")

if __name__ == "__main__":
    build_presentation()
