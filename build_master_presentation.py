import os
import shutil
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

MASTER_TEMPLATE = r"C:\Users\Himanshu Pathak\Downloads\Master Template for SIP (1).pptx"
OUT_10_WS = r"d:\AI INTERNSHIP\HimanshuPathak_UAI05BT12417_SIP_Presentation.pptx"
OUT_10_DL = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_UAI05BT12417_SIP_Presentation.pptx"

OUT_10_ALT_WS = r"d:\AI INTERNSHIP\HimanshuPathak_UAI05BT12417_SIP_Presentation_10Slides.pptx"
OUT_10_ALT_DL = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_UAI05BT12417_SIP_Presentation_10Slides.pptx"

OUT_12_WS = r"d:\AI INTERNSHIP\HimanshuPathak_UAI05BT12417_SIP_Presentation_12Slides.pptx"
OUT_12_DL = r"C:\Users\Himanshu Pathak\Downloads\HimanshuPathak_UAI05BT12417_SIP_Presentation_12Slides.pptx"

LOGO_IMG = r"d:\AI INTERNSHIP\sandesh_extracted_logo.png"
FIG1_1 = r"d:\AI INTERNSHIP\report_figures\fig1_1_methodology_flow.png"
FIG1_2 = r"d:\AI INTERNSHIP\report_figures\fig1_2_er_diagram.png"
FIG1_3 = r"d:\AI INTERNSHIP\report_figures\fig1_3_state_machine.png"
FIG_BENCHMARK = r"d:\AI INTERNSHIP\report_figures\fig_results_benchmark.png"
WORKFLOW_IMG = r"d:\AI INTERNSHIP\workflow_pipeline_diagram.png"

# Color Palette matching Master Template
COLOR_NAVY = RGBColor(0x0F, 0x17, 0x2A)   # #0F172A
COLOR_BLUE = RGBColor(0x1E, 0x3A, 0x8A)   # #1E3A8A
COLOR_SLATE = RGBColor(0x33, 0x41, 0x55)  # #334155
COLOR_MUTED = RGBColor(0x47, 0x55, 0x69)  # #475569
COLOR_LIGHT = RGBColor(0x64, 0x74, 0x8B)  # #64748B
COLOR_CARD_BG = RGBColor(0xF8, 0xFA, 0xFC) # #F8FAFC
COLOR_BORDER = RGBColor(0xE2, 0xE8, 0xF0)  # #E2E8F0
COLOR_RED = RGBColor(0xEF, 0x44, 0x44)
COLOR_GREEN = RGBColor(0x65, 0xA3, 0x0D)

FONT_NAME = "Inter"

def set_text(shape, text, font_name=FONT_NAME, font_size_pt=None, bold=None, color_rgb=None, align=None):
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    tf.word_wrap = True
    
    # Preserve formatting defaults if not supplied
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

def remove_shape(shape):
    sp = shape._element
    sp.getparent().remove(sp)

def replace_picture(slide, old_shape, new_img_path, target_left=None, target_top=None, target_width=None, target_height=None):
    l = target_left if target_left is not None else old_shape.left
    t = target_top if target_top is not None else old_shape.top
    w = target_width if target_width is not None else old_shape.width
    h = target_height if target_height is not None else old_shape.height
    
    remove_shape(old_shape)
    new_pic = slide.shapes.add_picture(new_img_path, l, t, w, h)
    return new_pic

def build_10_slide_presentation():
    print(f"Loading master template: {MASTER_TEMPLATE}")
    prs = Presentation(MASTER_TEMPLATE)
    
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
            set_text(shape, "4th May 2026 – 13th June 2026", font_size_pt=13.5, bold=False, color_rgb=COLOR_MUTED)
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
    pic_s2 = [s for s in s2.shapes if "PICTURE" in str(s.shape_type) or "Picture" in s.name]
    if pic_s2 and os.path.exists(LOGO_IMG):
        replace_picture(s2, pic_s2[0], LOGO_IMG, target_left=Inches(8.55), target_top=Inches(2.65), target_width=Inches(2.75), target_height=Inches(0.68))
        
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
    # Remove placeholder icon & text on right
    to_remove_s4 = [sh for sh in s4.shapes if sh.name in ["TextBox 19", "Picture 11"]]
    for sh in to_remove_s4:
        remove_shape(sh)
        
    # Place workflow / architecture image inside the right card
    if os.path.exists(WORKFLOW_IMG):
        s4.shapes.add_picture(WORKFLOW_IMG, Inches(7.95), Inches(1.80), Inches(4.95), Inches(3.80))
        
    for shape in s4.shapes:
        name = shape.name
        if name == "TextBox 85":
            set_text(shape, "Backend Architecture & Data Modeling", font_size_pt=16.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 87":
            set_text(shape, "Designed normalized relational schemas in SQLAlchemy ORM for Users, Profiles, Scores, and RiskAlerts across SQLite (WAL) and PostgreSQL.", font_size_pt=12.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 89":
            set_text(shape, "Clinical Scoring & Crisis Alert Pipeline", font_size_pt=16.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 91":
            set_text(shape, "Implemented DASS-21, BFI-44 (6 - R reverse keying), and automated server-side triggers for immediate counsellor crisis triage.", font_size_pt=12.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 93":
            set_text(shape, "SPA Frontend & ReportLab PDF Engine", font_size_pt=16.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 95":
            set_text(shape, "Built 11 React SPA dashboard views in Vite + TailwindCSS, and programmed dynamic ReportLab multi-page clinical diagnostic PDF generators.", font_size_pt=12.5, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 97":
            set_text(shape, "Machine Learning & System Orchestration", font_size_pt=16.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 99":
            set_text(shape, "Trained Random Forest models (R^2 = 0.912) on 50k samples served via FastAPI (Port 8000), and automated multi-process deployment scripts.", font_size_pt=12.5, bold=False, color_rgb=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 5: Project Overview
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    for shape in s5.shapes:
        name = shape.name
        if name == "TextBox 21":
            set_text(shape, "Dual-service ecosystem unifying clinical psychological assessment with machine learning lifestyle analytics.", font_size_pt=15.0, bold=False, color_rgb=COLOR_NAVY)
        elif name == "TextBox 35":
            set_text(shape, "Problem Statement & Solution", font_size_pt=15.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 36":
            set_text(shape, "\"Higher education institutions suffer from 3-14 day delays and error-prone manual reverse scoring in student mental health screening, with zero empirical correlation to daily lifestyle habits.\"", font_size_pt=14.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 25":
            set_text(shape, "Zero-Friction Ingestion: Mobile-responsive standalone web intake running on Port 5001.", font_size_pt=14.5, bold=True, color_rgb=COLOR_SLATE)
        elif name == "TextBox 27":
            set_text(shape, "Automated Scoring & Risk Engine: Exact DASS-21, BFI-44 (6 - R), and instant crisis flags.", font_size_pt=14.5, bold=True, color_rgb=COLOR_SLATE)
        elif name == "TextBox 29":
            set_text(shape, "Programmatic Clinical PDF Dossiers: Dynamic ReportLab rendering generated in under 850ms.", font_size_pt=14.5, bold=True, color_rgb=COLOR_SLATE)
        elif name == "TextBox 31":
            set_text(shape, "ProductivAI ML Analytics: FastAPI engine predicting productivity from sleep, study, and mood.", font_size_pt=14.5, bold=True, color_rgb=COLOR_SLATE)

    # -------------------------------------------------------------
    # SLIDE 6: Technologies & Tools Used
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    for shape in s6.shapes:
        name = shape.name
        if name == "TextBox 30":
            set_text(shape, "Frontend / Interface", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 32":
            set_text(shape, "React 18, Vite 5, TailwindCSS 3.4, Chart.js 4.4, Lucide", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 34":
            set_text(shape, "Core Backend", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 36":
            set_text(shape, "Python 3.13, Flask 3.0.0 (App Factory), FastAPI 0.109+", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 38":
            set_text(shape, "Database & Storage", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 40":
            set_text(shape, "Flask-SQLAlchemy, SQLite (WAL Mode), PostgreSQL 15", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 42":
            set_text(shape, "AI / Machine Learning", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 44":
            set_text(shape, "Scikit-Learn (Random Forest), Pandas, NumPy, Joblib", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 46":
            set_text(shape, "Authentication & Security", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 48":
            set_text(shape, "Flask-Login, Flask-Bcrypt, Flask-WTF (CSRF), Cookies", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 50":
            set_text(shape, "Reporting & DevOps", font_size_pt=15.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 52":
            set_text(shape, "ReportLab 4.1 (PDF), OpenPyXL, PowerShell / Batch, Git", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 7: Methodology & Workflow
    # -------------------------------------------------------------
    s7 = prs.slides[6]
    # Remove placeholder diagram shapes
    to_remove_s7 = [sh for sh in s7.shapes if sh.name in ["Picture 9", "TextBox 27", "TextBox 29"]]
    for sh in to_remove_s7:
        remove_shape(sh)
        
    # Insert Methodology Flow Diagram in the right container
    if os.path.exists(FIG1_1):
        s7.shapes.add_picture(FIG1_1, Inches(6.10), Inches(2.05), Inches(6.60), Inches(3.80))
        
    for shape in s7.shapes:
        name = shape.name
        if name == "TextBox 11":
            set_text(shape, "Phase 1: Requirements & Domain Analysis", font_size_pt=15.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 13":
            set_text(shape, "Analyzed Lovibond DASS-21 and John & Srivastava BFI-44 clinical norms; mapped scoring formulations.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 15":
            set_text(shape, "Phase 2: Relational Architecture & Modeling", font_size_pt=15.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 17":
            set_text(shape, "Designed 3NF database schema, decoupled microservices, and established RESTful API contracts.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 19":
            set_text(shape, "Phase 3: Core Implementation & ML Training", font_size_pt=15.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 21":
            set_text(shape, "Built app/scoring.py, ReportLab PDF generators, and trained Random Forest on 50k lifestyle rows.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 23":
            set_text(shape, "Phase 4: Integration, Testing & Deployment", font_size_pt=15.0, bold=True, color_rgb=COLOR_BLUE)
        elif name == "TextBox 25":
            set_text(shape, "Developed React SPA, executed unit/integration tests, and authored launch_all orchestrators.", font_size_pt=13.0, bold=False, color_rgb=COLOR_MUTED)
        elif name == "TextBox 30":
            set_text(shape, "", font_size_pt=1.0) # Clear hint

    # -------------------------------------------------------------
    # SLIDE 8: Key Contributions & Achievements
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    # Remove template placeholder box
    to_remove_s8 = [sh for sh in s8.shapes if sh.name == "TextBox 35"]
    for sh in to_remove_s8:
        remove_shape(sh)
        
    contributions = [
        ("Dual-Service Production Ecosystem",
         "Architected, developed, and deployed UAi PsychePortal (Ports 5000/5001) and ProductivAI ML engine (Port 8000) as an integrated clinical suite."),
        ("Zero Crisis Window Latency",
         "Eliminated 3-14 day manual triage delays by triggering automated emergency risk alerts in under 28ms upon severe assessment detection."),
        ("100% Algorithmic Scoring Fidelity",
         "Implemented flawless DASS-21 subscale math and BFI-44 6-R reverse scoring with verified 100% automated test coverage."),
        ("Automated Clinical Dossier Generation",
         "Built dynamic ReportLab PDF engine compiling multi-page diagnostic records in under 850ms, saving ~40 minutes per student evaluation."),
        ("High-Precision ML Productivity Model",
         "Trained Random Forest Regressor achieving R² = 0.912 and MAE = 3.42 on 50,000 records, served via FastAPI with sub-15ms inference."),
        ("One-Click Multi-Service Orchestration",
         "Authored unified PowerShell & Batch automation scripts with port collision detection, health checks, and cross-platform deployment.")
    ]
    
    # 2 columns x 3 rows grid
    coords = [
        (0.50, 1.97), (6.83, 1.97),
        (0.50, 3.44), (6.83, 3.44),
        (0.50, 4.92), (6.83, 4.92)
    ]
    
    card_w = 6.00
    card_h = 1.25
    
    for idx, (title, desc) in enumerate(contributions):
        left_in, top_in = coords[idx]
        # Rounded rectangle background
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_in), Inches(top_in), Inches(card_w), Inches(card_h))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_BORDER
        card.line.width = Pt(1)
        
        # Title text
        tb_t = s8.shapes.add_textbox(Inches(left_in + 0.25), Inches(top_in + 0.18), Inches(card_w - 0.5), Inches(0.28))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title
        r_t.font.name = FONT_NAME
        r_t.font.size = Pt(14.5)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_NAVY
        
        # Description text
        tb_d = s8.shapes.add_textbox(Inches(left_in + 0.25), Inches(top_in + 0.50), Inches(card_w - 0.5), Inches(0.68))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
        p_d = tf_d.paragraphs[0]
        r_d = p_d.add_run()
        r_d.text = desc
        r_d.font.name = FONT_NAME
        r_d.font.size = Pt(11.5)
        r_d.font.bold = False
        r_d.font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------
    # SLIDE 9: Challenges & Solutions
    # -------------------------------------------------------------
    s9 = prs.slides[8]
    for shape in s9.shapes:
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
    # SLIDE 10: Results & Impact
    # -------------------------------------------------------------
    s10 = prs.slides[9]
    # Remove placeholder shapes on slide 10
    to_remove_s10 = [sh for sh in s10.shapes if sh.name in ["Picture 5", "TextBox 7", "TextBox 9"]]
    for sh in to_remove_s10:
        remove_shape(sh)
        
    for shape in s10.shapes:
        name = shape.name
        if name == "TextBox 11":
            set_text(shape, "Results & Impact", font_size_pt=30.0, bold=True, color_rgb=COLOR_NAVY)
        elif name == "TextBox 32":
            set_text(shape, "Sub-15ms ML inference, 12ms clinical scoring, and 850ms dynamic PDF dossier generation.", font_size_pt=14.0, bold=False, color_rgb=COLOR_MUTED)
            shape.left = Inches(0.50)
            shape.top = Inches(1.48)
            shape.width = Inches(12.33)
        elif name == "TextBox 37":
            set_text(shape, "Reduced institutional crisis identification time from 14 days to real time, saving counsellors ~40 minutes per evaluation.", font_size_pt=14.0, bold=True, color_rgb=COLOR_NAVY)
            shape.left = Inches(0.50)
            shape.top = Inches(1.85)
            shape.width = Inches(12.33)
            
    # Position benchmark image in the bottom container
    if os.path.exists(FIG_BENCHMARK):
        s10.shapes.add_picture(FIG_BENCHMARK, Inches(0.65), Inches(2.40), Inches(12.00), Inches(4.10))

    # Save
    prs.save(OUT_10_WS)
    shutil.copyfile(OUT_10_WS, OUT_10_DL)
    shutil.copyfile(OUT_10_WS, OUT_10_ALT_WS)
    shutil.copyfile(OUT_10_WS, OUT_10_ALT_DL)
    print(f"Master 10-slide presentation successfully generated at:\n  - {OUT_10_WS}\n  - {OUT_10_DL}")

if __name__ == "__main__":
    build_10_slide_presentation()
