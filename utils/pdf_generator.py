import os
import numpy as np
from io import BytesIO
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748b'))
        
        # Separator line
        self.setStrokeColor(colors.HexColor('#e2e8f0'))
        self.setLineWidth(0.5)
        self.line(36, 40, 559, 40)
        
        footer_text = f"Confidential — Safe Space AI-Driven Analysis | UAi Psychology Department | Page {self._pageNumber} of {page_count}"
        self.drawCentredString(297.5, 25, footer_text)
        self.restoreState()

def get_bfi_radar_chart(scores_dict):
    labels = ['Extraversion', 'Agreeableness', 'Conscientiousness', 'Neuroticism', 'Openness']
    stats = [float(scores_dict.get(l, 3.0)) for l in labels]
    
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    stats += stats[:1]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(2.6, 2.6), subplot_kw=dict(polar=True))
    ax.fill(angles, stats, color='#0d9488', alpha=0.2)
    ax.plot(angles, stats, color='#0d9488', linewidth=1.5)
    
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=6.5, color='#334155', fontweight='bold')
    ax.spines['polar'].set_color('#cbd5e1')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf

def get_dass_bar_chart(scores_dict, severities_dict):
    labels = ['Depression', 'Anxiety', 'Stress']
    stats = [int(scores_dict.get(l, 0)) for l in labels]
    
    color_map = {
        "Normal": "#22c55e",
        "Mild": "#84cc16",
        "Moderate": "#f97316",
        "Severe": "#ef4444",
        "Extremely Severe": "#991b1b"
    }
    colors_list = [color_map.get(severities_dict.get(l, "Normal"), "#1a3a6b") for l in labels]
    
    fig, ax = plt.subplots(figsize=(2.8, 1.8))
    bars = ax.bar(labels, stats, color=colors_list, width=0.45, edgecolor='#e2e8f0', linewidth=0.5)
    
    ax.set_ylim(0, 42)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cbd5e1')
    ax.spines['bottom'].set_color('#cbd5e1')
    ax.tick_params(axis='both', colors='#475569', labelsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='#e2e8f0')
    ax.set_axisbelow(True)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 2),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=7, fontweight='bold', color='#334155')
                    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf

def generate_student_pdf(student_id):
    from app.models import StudentProfile, AssessmentSession, AssessmentScore, User
    from utils.report_text_generator import (
        generate_bfi_interpretation,
        generate_dass_interpretation,
        generate_dass_overall,
        generate_eq_sq_interpretation,
        generate_home_adjustment_interpretation,
        generate_integrated_summary
    )

    profile = StudentProfile.query.get(student_id)
    user = profile.user
    
    session_obj = AssessmentSession.query.filter_by(student_id=profile.id, status='completed').order_by(AssessmentSession.completed_at.desc()).first()
    if not session_obj:
        raise ValueError("No completed assessment session found.")
        
    scores = AssessmentScore.query.filter_by(session_id=session_obj.id).all()
    scores_by_assessment = {s.assessment.name: s for s in scores}
    
    # 1. BFI-44 Data
    bfi_sc = scores_by_assessment.get("BFI-44")
    bfi_scores, bfi_labels = {}, {}
    if bfi_sc and bfi_sc.category_scores:
        cs = bfi_sc.category_scores
        bfi_scores = cs.get("category_scores", {})
        bfi_labels = cs.get("severity_labels", {})
        opn_lvl = bfi_labels.get("Openness to Experience") or bfi_labels.get("Openness", "Moderate")
        bfi_labels["Openness"] = opn_lvl
        
    # 2. DASS-21 Data
    dass_sc = scores_by_assessment.get("DASS-21")
    dass_scores, dass_labels = {}, {}
    if dass_sc and dass_sc.category_scores:
        cs = dass_sc.category_scores
        dass_scores = cs.get("category_scores", {})
        dass_labels = cs.get("severity_labels", {})
        
    # 3. EQ-SQ Data
    eq_sc = scores_by_assessment.get("EQ")
    sq_sc = scores_by_assessment.get("SQ")
    eq_score_val = int(eq_sc.total_score) if eq_sc else 20
    sq_score_val = int(sq_sc.total_score) if sq_sc else 20
    eq_lvl = eq_sc.category_scores.get("severity_labels", {}).get("Emotional Awareness", "Moderate") if eq_sc else "Moderate"
    sq_lvl = sq_sc.category_scores.get("severity_labels", {}).get("Social Awareness", "Moderate") if sq_sc else "Moderate"
    
    # 4. Home Adjustment Data
    home_sc = scores_by_assessment.get("Home Adjustment Questionnaire")
    home_score_val = int(home_sc.total_score) if home_sc else 0
    if home_score_val <= 4:
        home_lvl = "Healthy Adjustment"
    elif home_score_val <= 9:
        home_lvl = "Mild Concerns"
    else:
        home_lvl = "Significant Difficulties"

    # ReportLab Document setup
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=54)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'SafeSpaceTitle',
        fontName='Times-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1a3a6b'),
        spaceAfter=2
    )
    subtitle_style = ParagraphStyle(
        'SafeSpaceSubtitle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=15
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        fontName='Times-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1a3a6b'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'ReportBody',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    bold_body_style = ParagraphStyle(
        'ReportBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    overall_style = ParagraphStyle(
        'OverallBox',
        parent=body_style,
        backColor=colors.HexColor('#f8fafc'),
        borderColor=colors.HexColor('#0d9488'),
        borderWidth=0.5,
        borderPadding=8,
        spaceBefore=8,
        spaceAfter=12
    )
    
    def get_color_span(lvl, text_type="level"):
        l = lvl.lower()
        if "high" in l or "severe" in l or "difficulties" in l:
            color = "#b91c1c" # red
        elif "moderate" in l or "mild" in l or "concerns" in l:
            color = "#d97706" # yellow
        else:
            color = "#15803d" # green
        return f'<font color="{color}"><b>{lvl}</b></font>'

    elements = []
    
    # 1. Header
    elements.append(Paragraph("Safe Space", title_style))
    elements.append(Paragraph("AI-Driven Analysis", subtitle_style))
    
    # 2. Student Details
    date_str = session_obj.completed_at.strftime('%Y-%m-%d') if session_obj.completed_at else "N/A"
    cohort_str = f"Batch {2025 - profile.year_of_study + 1}" if profile.year_of_study else "Batch 2025"
    details_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph(user.name, body_style),
         Paragraph("<b>Cohort:</b>", body_style), Paragraph(cohort_str, body_style)],
        [Paragraph("<b>Age / Gender:</b>", body_style), Paragraph(f"{profile.age}y / {profile.gender.capitalize() if profile.gender else 'N/A'}", body_style),
         Paragraph("<b>Date of Assessment:</b>", body_style), Paragraph(date_str, body_style)],
        [Paragraph("<b>Admission Number:</b>", body_style), Paragraph(user.uai_id, body_style),
         Paragraph("<b>Status:</b>", body_style), Paragraph("COMPLETED", bold_body_style)]
    ]
    details_table = Table(details_data, colWidths=[100, 160, 110, 150])
    details_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(details_table)
    elements.append(Spacer(1, 15))
    
    # 3. Section 1: BFI-44
    elements.append(Paragraph("Section 1: Big Five Personality Profile (BFI-44)", heading_style))
    
    # Score Table
    bfi_table_data = [[
        Paragraph("<b>Domain</b>", bold_body_style),
        Paragraph("<b>Score</b>", bold_body_style),
        Paragraph("<b>Level</b>", bold_body_style)
    ]]
    for d in ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"]:
        score = float(bfi_scores.get(d, 3.0))
        lvl = bfi_labels.get(d, "Moderate")
        bfi_table_data.append([
            Paragraph(d if d != "Openness" else "Openness to Experience", body_style),
            Paragraph(f"{score:.2f}", body_style),
            Paragraph(get_color_span(lvl), body_style)
        ])
    bfi_table = Table(bfi_table_data, colWidths=[130, 60, 70])
    bfi_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    
    # Radar chart Image
    bfi_chart_buf = get_bfi_radar_chart(bfi_scores)
    bfi_chart_img = Image(bfi_chart_buf, width=150, height=150)
    
    # Grid Table
    sec1_layout = Table([[bfi_table, bfi_chart_img]], colWidths=[270, 250])
    sec1_layout.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (1,0), (1,0), 30),
    ]))
    elements.append(sec1_layout)
    elements.append(Spacer(1, 10))
    
    # Interpretations
    for d in ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"]:
        lvl = bfi_labels.get(d, "Moderate")
        interp = generate_bfi_interpretation(d, lvl)
        label_name = d if d != "Openness" else "Openness to Experience"
        elements.append(Paragraph(f"<b>{label_name}:</b> {interp}", body_style))
        
    elements.append(Paragraph(f"<b>Overall Personality Profile:</b> The personality profile suggests that the student's behavioural style, emotional functioning, and interpersonal tendencies are shaped by the above personality characteristics. These traits may influence academic adjustment, peer relationships, coping styles, and response to challenges.", overall_style))
    
    # 4. Section 2: DASS-21
    elements.append(Paragraph("Section 2: DASS-21 Emotional Scales", heading_style))
    
    # Score Table
    dass_table_data = [[
        Paragraph("<b>Domain</b>", bold_body_style),
        Paragraph("<b>Score</b>", bold_body_style),
        Paragraph("<b>Severity</b>", bold_body_style)
    ]]
    for s in ["Depression", "Anxiety", "Stress"]:
        score = int(dass_scores.get(s, 0))
        sev = dass_labels.get(s, "Normal")
        dass_table_data.append([
            Paragraph(s, body_style),
            Paragraph(str(score), body_style),
            Paragraph(get_color_span(sev), body_style)
        ])
    dass_table = Table(dass_table_data, colWidths=[130, 60, 70])
    dass_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    
    # Bar Chart Image
    dass_chart_buf = get_dass_bar_chart(dass_scores, dass_labels)
    dass_chart_img = Image(dass_chart_buf, width=150, height=110)
    
    # Grid Table
    sec2_layout = Table([[dass_table, dass_chart_img]], colWidths=[270, 250])
    sec2_layout.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (1,0), (1,0), 30),
    ]))
    elements.append(sec2_layout)
    elements.append(Spacer(1, 10))
    
    # Interpretations
    for s in ["Depression", "Anxiety", "Stress"]:
        sev = dass_labels.get(s, "Normal")
        interp = generate_dass_interpretation(s, sev)
        elements.append(Paragraph(f"<b>{s}:</b> {interp}", body_style))
        
    elements.append(Paragraph(f"<b>Overall Emotional Well-being:</b> {generate_dass_overall(dass_labels)}", overall_style))
    
    # 5. Section 3: EQ-SQ
    elements.append(Paragraph("Section 3: EQ-SQ Social-Emotional Quotients", heading_style))
    
    eq_sq_table_data = [
        [Paragraph("<b>Domain</b>", bold_body_style), Paragraph("<b>Score (0-40)</b>", bold_body_style), Paragraph("<b>Level</b>", bold_body_style)],
        [Paragraph("Emotional Quotient (EQ)", body_style), Paragraph(f"{eq_score_val} / 40", body_style), Paragraph(get_color_span(eq_lvl), body_style)],
        [Paragraph("Social Quotient (SQ)", body_style), Paragraph(f"{sq_score_val} / 40", body_style), Paragraph(get_color_span(sq_lvl), body_style)]
    ]
    eq_sq_table = Table(eq_sq_table_data, colWidths=[180, 100, 100])
    eq_sq_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(eq_sq_table)
    elements.append(Spacer(1, 8))
    
    eq_p, sq_p, overall_eq_sq_p = generate_eq_sq_interpretation(eq_lvl, sq_lvl)
    elements.append(Paragraph(f"<b>EQ:</b> {eq_p}", body_style))
    elements.append(Paragraph(f"<b>SQ:</b> {sq_p}", body_style))
    elements.append(Paragraph(f"<b>Overall Emotional & Social Functioning:</b> {overall_eq_sq_p}", overall_style))
    
    # 6. Section 4: Home Adjustment
    elements.append(Paragraph("Section 4: Home & Family Adjustment", heading_style))
    elements.append(Paragraph(f"<b>Home Adjustment Score:</b> {home_score_val} / 15 — {get_color_span(home_lvl)}", body_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(generate_home_adjustment_interpretation(home_lvl), body_style))
    elements.append(Spacer(1, 10))
    
    # 7. Section 5: Integrated Summary
    summary_data = {
        "bfi": {"levels": bfi_labels},
        "dass": {"levels": dass_labels},
        "eq_sq": {"eq_level": eq_lvl, "sq_level": sq_lvl},
        "home": {"level": home_lvl}
    }
    elements.append(Paragraph("Section 5: Integrated Clinical Summary", heading_style))
    elements.append(Paragraph(generate_integrated_summary(summary_data), body_style))
    
    doc.build(elements, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer
