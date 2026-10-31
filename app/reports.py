import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing, Rect, String
from .models import User, StudentProfile, AssessmentSession, AssessmentScore, Assessment, Response, Question, Flag, db
from datetime import datetime

def generate_pdf_report(student_id):
    student = User.query.get(student_id)
    profile = student.student_profile
    latest_session = AssessmentSession.query.filter_by(student_id=profile.id, status='completed').order_by(AssessmentSession.completed_at.desc()).first()
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Page 1: Cover Page
    elements.append(Paragraph("University Psychology Portal", styles['Heading1']))
    elements.append(Spacer(1, 100))
    elements.append(Paragraph("Confidential Psychological Assessment Report", styles['Title']))
    elements.append(Spacer(1, 50))
    
    cover_data = [
        ["Student Name:", student.name],
        ["UAi ID:", student.uai_id],
        ["Department:", profile.department],
        ["Assessment Date:", latest_session.completed_at.strftime('%Y-%m-%d') if latest_session else "N/A"],
        ["Counsellor:", profile.assigned_counsellor.name if profile.assigned_counsellor else "Unassigned"]
    ]
    t = Table(cover_data, colWidths=[150, 250])
    t.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 12)]))
    elements.append(t)
    
    elements.append(Spacer(1, 300))
    elements.append(Paragraph("Confidentiality Notice: This report contains sensitive information. Do not share without authorization.", styles['Italic']))
    elements.append(PageBreak())

    # Page 2: Student Profile
    elements.append(Paragraph("Student Profile", styles['Heading2']))
    elements.append(Spacer(1, 20))
    profile_data = [
        ["Age", profile.age],
        ["Gender", profile.gender],
        ["Year of Study", profile.year_of_study],
        ["Course", profile.course],
        ["Consent Date", profile.consent_timestamp.strftime('%Y-%m-%d %H:%M') if profile.consent_timestamp else "N/A"],
        ["Total Duration", f"{latest_session.total_time_seconds // 60}m {latest_session.total_time_seconds % 60}s" if latest_session else "N/A"]
    ]
    t2 = Table(profile_data, colWidths=[150, 250])
    t2.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.grey), ('BACKGROUND', (0,0), (0,-1), colors.lightgrey)]))
    elements.append(t2)
    elements.append(PageBreak())

    # Page 3: DASS-21 Results
    if latest_session:
        dass_score = AssessmentScore.query.filter_by(session_id=latest_session.id).join(Assessment).filter(Assessment.name == 'DASS-21').first()
        if dass_score:
            elements.append(Paragraph("DASS-21 Results", styles['Heading2']))
            elements.append(Spacer(1, 20))
            
            def get_color(severity):
                sev = severity.lower()
                if 'normal' in sev: return colors.green
                if 'mild' in sev: return colors.yellow
                if 'moderate' in sev: return colors.orange
                return colors.red

            dass_table = [["Subscale", "Raw Score", "Severity"]]
            cat_scores = dass_score.category_scores or {}
            
            # Check if this is the new nested format or the old flat format
            if "category_scores" in cat_scores:
                scores = cat_scores["category_scores"]
                severities = cat_scores["severity_labels"]
                dep_score_val = scores.get("Depression", 0)
                dep_sev_val = severities.get("Depression", "Normal")
                anx_score_val = scores.get("Anxiety", 0)
                anx_sev_val = severities.get("Anxiety", "Normal")
                str_score_val = scores.get("Stress", 0)
                str_sev_val = severities.get("Stress", "Normal")
                
                dass_table.append(["Depression", dep_score_val, dep_sev_val])
                dass_table.append(["Anxiety", anx_score_val, anx_sev_val])
                dass_table.append(["Stress", str_score_val, str_sev_val])
            else:
                dep_score_val = cat_scores.get('depression', {}).get('score', 0)
                dep_sev_val = cat_scores.get('depression', {}).get('severity', 'Normal')
                anx_score_val = cat_scores.get('anxiety', {}).get('score', 0)
                anx_sev_val = cat_scores.get('anxiety', {}).get('severity', 'Normal')
                str_score_val = cat_scores.get('stress', {}).get('score', 0)
                str_sev_val = cat_scores.get('stress', {}).get('severity', 'Normal')
                
                dass_table.append(["Depression", dep_score_val, dep_sev_val])
                dass_table.append(["Anxiety", anx_score_val, anx_sev_val])
                dass_table.append(["Stress", str_score_val, str_sev_val])
            
            t3 = Table(dass_table, colWidths=[130, 130, 140])
            t3.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('GRID', (0,0), (-1,-1), 1, colors.grey),
                ('BACKGROUND', (2,1), (2,1), get_color(dep_sev_val)),
                ('BACKGROUND', (2,2), (2,2), get_color(anx_sev_val)),
                ('BACKGROUND', (2,3), (2,3), get_color(str_sev_val)),
            ]))
            elements.append(t3)
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("The DASS-21 measures negative emotional states. Scores represent severity levels based on standardized norms.", styles['BodyText']))
    elements.append(PageBreak())

    # Page 4: BFI-44 Big Five Profile
    if latest_session:
        bfi_score = AssessmentScore.query.filter_by(session_id=latest_session.id).join(Assessment).filter(Assessment.name == 'BFI-44').first()
        if bfi_score:
            elements.append(Paragraph("BFI-44 Big Five Personality Profile", styles['Heading2']))
            elements.append(Spacer(1, 20))
            
            bfi_table = [["Trait", "Level"]]
            cat_scores = bfi_score.category_scores or {}
            
            # Check if this is the new nested format or the old flat format
            if "category_scores" in cat_scores:
                levels = cat_scores["severity_labels"]
                for trait in ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"]:
                    bfi_table.append([trait, levels.get(trait, "Moderate")])
            else:
                for trait, res in cat_scores.items():
                    bfi_table.append([trait.capitalize(), res.get('level', "Moderate")])
                
            t4 = Table(bfi_table, colWidths=[200, 200])
            t4.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('GRID', (0,0), (-1,-1), 1, colors.grey),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
            ]))
            elements.append(t4)
    elements.append(PageBreak())

    # Page 5: EQ & SQ Scores
    if latest_session:
        eq_score = AssessmentScore.query.filter_by(session_id=latest_session.id).join(Assessment).filter(Assessment.name == 'EQ').first()
        sq_score = AssessmentScore.query.filter_by(session_id=latest_session.id).join(Assessment).filter(Assessment.name == 'SQ').first()
        
        elements.append(Paragraph("EQ & SQ Scores", styles['Heading2']))
        elements.append(Spacer(1, 20))
        
        eq_sq_data = [
            [f"Empathy Quotient (EQ): {eq_score.total_score if eq_score else 'N/A'}", 
             f"Systemizing Quotient (SQ): {sq_score.total_score if sq_score else 'N/A'}"],
            [f"Category: {eq_score.severity_label if eq_score else 'N/A'}", 
             f"Category: {sq_score.severity_label if sq_score else 'N/A'}"]
        ]
        t5 = Table(eq_sq_data, colWidths=[200, 200])
        t5.setStyle(TableStyle([('BOX', (0,0), (0,-1), 2, colors.teal), ('BOX', (1,0), (1,-1), 2, colors.purple), ('PADDING', (0,0), (-1,-1), 10)]))
        elements.append(t5)
    elements.append(PageBreak())

    # Page 6: Recommendations
    elements.append(Paragraph("Summary & Recommendations", styles['Heading2']))
    elements.append(Spacer(1, 20))
    risk = profile.risk_level or "Normal"
    risk_color = colors.green if risk == "Normal" else (colors.yellow if risk == "Mild" else (colors.orange if risk == "Moderate" else colors.red))
    
    rec_style = ParagraphStyle('RecStyle', parent=styles['BodyText'], backColor=risk_color, borderPadding=10, textColor=colors.white if risk in ["Moderate", "Severe"] else colors.black)
    elements.append(Paragraph(f"Overall Risk Level: {risk}", rec_style))
    elements.append(Spacer(1, 20))
    
    recs = {
        "Normal": "No immediate intervention required. Monitor periodically.",
        "Mild": "Recommend brief check-in with counsellor.",
        "Moderate": "Schedule counselling session within 2 weeks.",
        "Severe": "Immediate counsellor intervention recommended."
    }
    elements.append(Paragraph(recs.get(risk, recs["Normal"]), styles['BodyText']))
    
    # Page 7+: Itemized Assessment Responses (Question-by-Question Exact Scores)
    if latest_session:
        elements.append(PageBreak())
        elements.append(Paragraph("Itemized Assessment Responses", styles['Heading2']))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("Below is the complete question-by-question log of student answers and option values.", styles['BodyText']))
        elements.append(Spacer(1, 15))
        
        # Query all questions and responses in order
        all_questions = Question.query.join(Assessment).order_by(Assessment.id, Question.order_number).all()
        all_responses = Response.query.filter_by(session_id=latest_session.id).all()
        resp_map_all = {r.question_id: r for r in all_responses}
        
        table_data = [["Q#", "Section", "Question Text", "Score"]]
        
        for idx, q in enumerate(all_questions):
            r = resp_map_all.get(q.id)
            selected_val = "—"
            if r and r.selected_option is not None:
                selected_val = str(r.selected_option)
                
            sec_name = "Other"
            if q.assessment.name == "DASS-21":
                sec_name = "Sec 1 (DASS)"
            elif q.assessment.name == "BFI-44":
                sec_name = "Sec 2 (BFI)"
            elif q.assessment.name == "EQ":
                sec_name = "Sec 3 (EQ)"
            elif q.assessment.name == "SQ":
                sec_name = "Sec 4 (SQ)"
            elif q.assessment.name == "UAI Psychology Quiz":
                sec_name = "Sec 5 (UAI)"
            elif q.assessment.name == "Home Adjustment Questionnaire":
                sec_name = "Sec 6 (Home)"
                
            short_q = q.question_text
            if len(short_q) > 85:
                short_q = short_q[:82] + "..."
                
            table_data.append([
                f"Q{idx + 1}",
                sec_name,
                short_q,
                selected_val
            ])
            
        t_resp = Table(table_data, colWidths=[35, 75, 330, 40])
        t_resp.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (1,-1), 'LEFT'),
            ('ALIGN', (3,0), (3,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        elements.append(t_resp)
        
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_excel_report(counsellor_id):
    students = StudentProfile.query.filter_by(assigned_counsellor_id=counsellor_id).all()
    
    summary_rows = []
    flagged_rows = []
    
    for s in students:
        u = s.user
        latest_session = AssessmentSession.query.filter_by(student_id=s.id, status='completed').order_by(AssessmentSession.completed_at.desc()).first()
        
        row = {
            "UAi ID": u.uai_id,
            "Name": u.name,
            "Dept": s.department,
            "Year": s.year_of_study,
            "Risk Level": s.risk_level or "Normal",
            "Flagged": "Yes" if Flag.query.filter_by(student_id=u.id, is_resolved=False).first() else "No"
        }
        
        if latest_session:
            scores = AssessmentScore.query.filter_by(session_id=latest_session.id).all()
            for sc in scores:
                if sc.assessment.name == 'DASS-21':
                    row["DASS-Depression"] = sc.category_scores['depression']['score']
                    row["DASS-Anxiety"] = sc.category_scores['anxiety']['score']
                    row["DASS-Stress"] = sc.category_scores['stress']['score']
                elif sc.assessment.name == 'BFI-44':
                    row["BFI-O"] = sc.category_scores['openness']['score']
                    row["BFI-C"] = sc.category_scores['conscientiousness']['score']
                    row["BFI-E"] = sc.category_scores['extraversion']['score']
                    row["BFI-A"] = sc.category_scores['agreeableness']['score']
                    row["BFI-N"] = sc.category_scores['neuroticism']['score']
                elif sc.assessment.name == 'EQ':
                    row["EQ"] = sc.total_score
                elif sc.assessment.name == 'SQ':
                    row["SQ"] = sc.total_score
        
        summary_rows.append(row)
        
        # Flags
        flags = Flag.query.filter_by(student_id=u.id, is_resolved=False).all()
        for f in flags:
            flagged_rows.append({
                "Name": u.name,
                "Risk Level": s.risk_level or "Normal",
                "Flag Reason": f.reason,
                "Flag Date": f.created_at.strftime('%Y-%m-%d')
            })

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_summary = pd.DataFrame(summary_rows)
        df_summary.to_excel(writer, index=False, sheet_name='Summary')
        
        df_flagged = pd.DataFrame(flagged_rows)
        df_flagged.to_excel(writer, index=False, sheet_name='Flagged Students')
        
        # Formatting (Simplified)
        workbook = writer.book
        for sheetname in ['Summary', 'Flagged Students']:
            worksheet = workbook[sheetname]
            for col in worksheet.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except: pass
                worksheet.column_dimensions[column].width = max_length + 2

    output.seek(0)
    return output
