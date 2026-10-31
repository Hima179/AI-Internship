import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('report_figures', exist_ok=True)

# ---------------------------------------------------------------------------
# FIGURE 1.1: Development Methodology Flow
# ---------------------------------------------------------------------------
def generate_fig1_1():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    stages = [
        ("STAGE 1\nRequirements &\nDomain Mapping", 
         ["Clinical protocol analysis", "DASS-21 / BFI-44 metrics", "Productivity feature scope"],
         "#1E3A8A"),
        ("STAGE 2\nArchitecture &\nData Modeling", 
         ["Relational schema design", "Flask & FastAPI backends", "React SPA wireframing"],
         "#0284C7"),
        ("STAGE 3\nImplementation &\nML Engineering", 
         ["Scoring algorithms (app/scoring.py)", "RandomForest ML training", "ReportLab dynamic PDF"],
         "#0D9488"),
        ("STAGE 4\nTesting, Integration\n& Deployment", 
         ["Multi-tiered testing suite", "Orchestrator scripts (bat/ps1)", "Counsellor dashboard deploy"],
         "#16A34A")
    ]

    box_w = 2.0
    box_h = 3.6
    spacing = 0.4
    start_x = 0.4

    for i, (title, points, color) in enumerate(stages):
        x = start_x + i * (box_w + spacing)
        y = 0.4
        
        # Header rect
        rect_head = patches.FancyBboxPatch((x, y + box_h - 1.1), box_w, 1.1,
                                           boxstyle="round,pad=0.04,rounding_size=0.08",
                                           facecolor=color, edgecolor="none")
        ax.add_patch(rect_head)
        ax.text(x + box_w/2, y + box_h - 0.55, title, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white', family='sans-serif', multialignment='center')

        # Body rect
        rect_body = patches.FancyBboxPatch((x, y), box_w, box_h - 1.15,
                                           boxstyle="round,pad=0.04,rounding_size=0.08",
                                           facecolor='#F8FAFC', edgecolor=color, linewidth=1.5)
        ax.add_patch(rect_body)

        # Bullets
        for j, pt in enumerate(points):
            py = y + box_h - 1.5 - (j * 0.7)
            ax.plot(x + 0.2, py, marker='o', markersize=4, color=color)
            ax.text(x + 0.35, py, pt, fontsize=7.2, color='#1E293B', family='sans-serif',
                    va='center', wrap=True)

        # Arrow to next stage
        if i < len(stages) - 1:
            ax.annotate('', xy=(x + box_w + spacing - 0.05, y + box_h / 2),
                        xytext=(x + box_w + 0.05, y + box_h / 2),
                        arrowprops=dict(facecolor='#475569', edgecolor='none', width=2.5, headwidth=7))

    plt.tight_layout()
    outpath = os.path.join('report_figures', 'fig1_1_methodology_flow.png')
    plt.savefig(outpath, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"Generated {outpath}")

# ---------------------------------------------------------------------------
# FIGURE 1.2: Entity-Relationship Diagram
# ---------------------------------------------------------------------------
def generate_fig1_2():
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    entities = [
        (0.5, 2.8, "USER", ["id (PK, Integer)", "username (String, Unique)", "password_hash (String)", "role (Enum: Admin/User)", "created_at (DateTime)"], "#1E3A8A"),
        (3.8, 2.8, "STUDENT_PROFILE", ["id (PK, Integer)", "user_id (FK -> User.id)", "roll_no (String, Unique)", "full_name (String)", "department (String)", "semester (Integer)"], "#0284C7"),
        (7.2, 2.8, "ASSESSMENT", ["id (PK, Integer)", "student_id (FK -> Profile.id)", "assessment_type (Enum)", "status (Completed/Flagged)", "created_at (DateTime)"], "#0D9488"),
        (0.5, 0.3, "PRODUCTIVITY_LOG", ["id (PK, Integer)", "user_id (FK -> User.id)", "sleep_hours (Float)", "study_hours (Float)", "screen_time (Float)", "predicted_score (Float)"], "#6366F1"),
        (3.8, 0.3, "SUBSCALE_SCORE", ["id (PK, Integer)", "assessment_id (FK -> Assmt.id)", "subscale_name (String)", "raw_score (Float)", "severity_category (String)"], "#D97706"),
        (7.2, 0.3, "RISK_ALERT", ["id (PK, Integer)", "assessment_id (FK -> Assmt.id)", "severity_level (Moderate/Severe)", "alert_message (Text)", "is_resolved (Boolean)"], "#DC2626")
    ]

    box_w = 2.4
    box_h = 1.9

    for x, y, name, fields, color in entities:
        h_rect = patches.FancyBboxPatch((x, y + box_h - 0.45), box_w, 0.45,
                                        boxstyle="round,pad=0.02,rounding_size=0.06",
                                        facecolor=color, edgecolor="none")
        ax.add_patch(h_rect)
        ax.text(x + box_w/2, y + box_h - 0.22, name, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white', family='sans-serif')

        b_rect = patches.FancyBboxPatch((x, y), box_w, box_h - 0.45,
                                        boxstyle="round,pad=0.02,rounding_size=0.06",
                                        facecolor='#F8FAFC', edgecolor=color, linewidth=1.2)
        ax.add_patch(b_rect)

        for idx, f in enumerate(fields):
            fy = y + box_h - 0.7 - (idx * 0.23)
            ax.text(x + 0.1, fy, f, fontsize=6.8, color='#1E293B', family='monospace')

    ax.annotate('', xy=(3.8, 3.8), xytext=(2.9, 3.8),
                arrowprops=dict(facecolor='#475569', edgecolor='none', width=1.5, headwidth=5))
    ax.text(3.35, 3.95, "1 : 1", fontsize=7, color='#475569', ha='center', fontweight='bold')

    ax.annotate('', xy=(7.2, 3.8), xytext=(6.2, 3.8),
                arrowprops=dict(facecolor='#475569', edgecolor='none', width=1.5, headwidth=5))
    ax.text(6.7, 3.95, "1 : N", fontsize=7, color='#475569', ha='center', fontweight='bold')

    ax.annotate('', xy=(1.7, 2.2), xytext=(1.7, 2.8),
                arrowprops=dict(facecolor='#475569', edgecolor='none', width=1.5, headwidth=5))
    ax.text(1.9, 2.5, "1 : N", fontsize=7, color='#475569', va='center', fontweight='bold')

    ax.annotate('', xy=(5.0, 2.2), xytext=(7.8, 2.8),
                arrowprops=dict(facecolor='#475569', edgecolor='none', width=1.5, headwidth=5))
    ax.text(6.6, 2.45, "1 : N", fontsize=7, color='#475569', ha='center', fontweight='bold')

    ax.annotate('', xy=(8.4, 2.2), xytext=(8.4, 2.8),
                arrowprops=dict(facecolor='#DC2626', edgecolor='none', width=1.5, headwidth=5))
    ax.text(8.7, 2.5, "1 : N", fontsize=7, color='#DC2626', va='center', fontweight='bold')

    plt.tight_layout()
    outpath = os.path.join('report_figures', 'fig1_2_er_diagram.png')
    plt.savefig(outpath, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"Generated {outpath}")

# ---------------------------------------------------------------------------
# FIGURE 1.3: Clinical Scoring & Risk State Machine
# ---------------------------------------------------------------------------
def generate_fig1_3():
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis('off')

    rect1 = patches.FancyBboxPatch((0.4, 1.6), 1.6, 1.2, boxstyle="round,pad=0.03,rounding_size=0.08",
                                   facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=1.5)
    ax.add_patch(rect1)
    ax.text(1.2, 2.4, "STATE 1", fontsize=7.5, fontweight='bold', color='#1E40AF', ha='center')
    ax.text(1.2, 1.95, "Assessment\nSubmitted\n(Port 5001)", fontsize=7.5, color='#1E293B', ha='center')

    ax.annotate('', xy=(2.4, 2.2), xytext=(2.0, 2.2),
                arrowprops=dict(facecolor='#475569', edgecolor='none', width=1.5, headwidth=5))

    rect2 = patches.FancyBboxPatch((2.4, 1.6), 1.8, 1.2, boxstyle="round,pad=0.03,rounding_size=0.08",
                                   facecolor="#F0FDF4", edgecolor="#16A34A", linewidth=1.5)
    ax.add_patch(rect2)
    ax.text(3.3, 2.4, "STATE 2", fontsize=7.5, fontweight='bold', color='#15803D', ha='center')
    ax.text(3.3, 1.95, "Clinical Scoring &\nReverse Coding\n(6 - R Matrix)", fontsize=7.5, color='#1E293B', ha='center')

    ax.annotate('', xy=(4.6, 2.2), xytext=(4.2, 2.2),
                arrowprops=dict(facecolor='#475569', edgecolor='none', width=1.5, headwidth=5))

    rect3 = patches.FancyBboxPatch((4.6, 1.6), 1.8, 1.2, boxstyle="round,pad=0.03,rounding_size=0.08",
                                   facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.5)
    ax.add_patch(rect3)
    ax.text(5.5, 2.4, "STATE 3", fontsize=7.5, fontweight='bold', color='#B45309', ha='center')
    ax.text(5.5, 1.95, "Norm Threshold\nEvaluation\n(DASS-21 / EQ)", fontsize=7.5, color='#1E293B', ha='center')

    ax.annotate('', xy=(6.9, 3.1), xytext=(6.4, 2.5),
                arrowprops=dict(facecolor='#DC2626', edgecolor='none', width=1.5, headwidth=5))
    ax.text(6.4, 3.0, "Score >= Mod", fontsize=6.8, color='#DC2626', fontweight='bold', ha='right')

    rect4a = patches.FancyBboxPatch((6.9, 2.6), 1.8, 1.1, boxstyle="round,pad=0.03,rounding_size=0.08",
                                    facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=1.5)
    ax.add_patch(rect4a)
    ax.text(7.8, 3.3, "EMERGENCY FLAG", fontsize=7.5, fontweight='bold', color='#B91C1C', ha='center')
    ax.text(7.8, 2.9, "Push Alert to\nDashboard (Port 5000)", fontsize=7.2, color='#1E293B', ha='center')

    ax.annotate('', xy=(6.9, 1.2), xytext=(6.4, 1.8),
                arrowprops=dict(facecolor='#16A34A', edgecolor='none', width=1.5, headwidth=5))
    ax.text(6.4, 1.3, "Score < Mod", fontsize=6.8, color='#16A34A', fontweight='bold', ha='right')

    rect4b = patches.FancyBboxPatch((6.9, 0.7), 1.8, 1.1, boxstyle="round,pad=0.03,rounding_size=0.08",
                                    facecolor="#F1F5F9", edgecolor="#64748B", linewidth=1.5)
    ax.add_patch(rect4b)
    ax.text(7.8, 1.4, "NORMAL ARCHIVE", fontsize=7.5, fontweight='bold', color='#334155', ha='center')
    ax.text(7.8, 1.0, "Standard Profile\nRecord Logged", fontsize=7.2, color='#1E293B', ha='center')

    ax.annotate('', xy=(9.0, 2.2), xytext=(8.7, 2.8),
                arrowprops=dict(facecolor='#475569', edgecolor='none', width=1.2, headwidth=4))
    ax.annotate('', xy=(9.0, 2.2), xytext=(8.7, 1.5),
                arrowprops=dict(facecolor='#475569', edgecolor='none', width=1.2, headwidth=4))

    rect5 = patches.FancyBboxPatch((9.0, 1.6), 0.9, 1.2, boxstyle="round,pad=0.03,rounding_size=0.08",
                                   facecolor="#EDE9FE", edgecolor="#7C3AED", linewidth=1.5)
    ax.add_patch(rect5)
    ax.text(9.45, 2.4, "REPORT", fontsize=7.2, fontweight='bold', color='#6D28D9', ha='center')
    ax.text(9.45, 1.95, "ReportLab\nPDF Build", fontsize=7.0, color='#1E293B', ha='center')

    plt.tight_layout()
    outpath = os.path.join('report_figures', 'fig1_3_state_machine.png')
    plt.savefig(outpath, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"Generated {outpath}")

# ---------------------------------------------------------------------------
# FIGURE 1.4: Testing Strategy Pyramid
# ---------------------------------------------------------------------------
def generate_fig1_4():
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=300)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 4.6)
    ax.axis('off')

    tiers = [
        (3.3, 4.2, 3.2, 5.8, 3.8, 5.2, "End-to-End Orchestration Tests", "launch_all.bat multi-service verification across ports 5000, 5001, 8000", "#DC2626"),
        (2.3, 3.2, 2.4, 6.6, 3.2, 5.8, "Security & Route Protection Tests", "Flask-Login sessions, Bcrypt auth, CSRF tokens, unauthenticated redirects", "#D97706"),
        (1.3, 2.2, 1.6, 7.4, 2.4, 6.6, "API & Integration Tests", "Intake JSON validation, ReportLab PDF rendering, FastAPI model inference", "#0284C7"),
        (0.3, 1.2, 0.8, 8.2, 1.6, 7.4, "Unit & Mathematical Scoring Tests", "DASS-21/BFI-44 reverse coding (6 - R), SQLAlchemy ORM constraints, neutral defaults", "#1E3A8A")
    ]

    for yb, yt, xlb, xrb, xlt, xrt, title, desc, color in tiers:
        poly = patches.Polygon([[xlb, yb], [xrb, yb], [xrt, yt], [xlt, yt]],
                               closed=True, facecolor=color, edgecolor='white', linewidth=1.5)
        ax.add_patch(poly)

        mid_y = (yb + yt) / 2
        ax.text(4.5, mid_y + 0.14, title, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white', family='sans-serif')
        ax.text(4.5, mid_y - 0.18, desc, ha='center', va='center',
                fontsize=6.8, color='#E2E8F0', family='sans-serif')

    plt.tight_layout()
    outpath = os.path.join('report_figures', 'fig1_4_testing_pyramid.png')
    plt.savefig(outpath, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"Generated {outpath}")

if __name__ == '__main__':
    generate_fig1_1()
    generate_fig1_2()
    generate_fig1_3()
    generate_fig1_4()
    print("All report figures generated successfully.")
