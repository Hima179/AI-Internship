from flask import render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_required, current_user
from . import counsellor
from ..auth import role_required
from ..models import User, StudentProfile, AssessmentSession, AssessmentScore, Response, Question, Flag, Assessment, db
from ..reports import generate_pdf_report, generate_excel_report
from sqlalchemy import or_
from datetime import datetime, timedelta
import json

@counsellor.route('/dashboard')
@login_required
@role_required('counsellor')
def dashboard():
    # Base query for assigned students
    assigned_students = StudentProfile.query.filter_by(assigned_counsellor_id=current_user.id).all()
    student_ids = [s.id for s in assigned_students]
    user_ids = [s.user_id for s in assigned_students]

    if not student_ids:
        # Default empty payload if no students
        return render_template('counsellor/dashboard.html', 
                               kpis={'total_assessed':0, 'flagged':0, 'moderate_stress':0, 'high_neuroticism':0, 'low_eq_risk':0}, 
                               chart_data={'overall_risk': {'labels': [], 'data': [], 'percentages': []}, 'domain_overview': {'labels': [], 'data': []}, 'cohort_risk': {'labels': [], 'low': [], 'moderate': [], 'high': [], 'severe': []}, 'trend': {'labels': [], 'data': []}}, 
                               flagged_students=[])

    # 1. KPIs
    total_assessed = AssessmentSession.query.filter(AssessmentSession.student_id.in_(student_ids), AssessmentSession.status == 'completed').count()
    flagged = Flag.query.filter(Flag.counsellor_id==current_user.id, Flag.is_resolved==False).count()
    moderate_stress = StudentProfile.query.filter(StudentProfile.id.in_(student_ids), StudentProfile.risk_level == 'Moderate').count()
    
    high_impulsivity = 0
    behavioural_risk = 0
    scores = AssessmentScore.query.join(AssessmentSession).filter(AssessmentSession.student_id.in_(student_ids)).all()
    for score in scores:
        if score.assessment.name == 'BFI-44':
            if score.category_scores and score.category_scores.get('neuroticism', {}).get('level') == 'High':
                high_impulsivity += 1
        elif score.assessment.name == 'EQ':
            if score.severity_label == 'Low':
                behavioural_risk += 1

    kpis = {
        'total_assessed': total_assessed,
        'flagged': flagged,
        'moderate_stress': moderate_stress,
        'high_impulsivity': high_impulsivity,
        'behavioural_risk': behavioural_risk
    }

    # 2. Chart Data
    risk_counts = {'Normal': 0, 'Mild': 0, 'Moderate': 0, 'Severe': 0}
    for s in assigned_students:
        if s.risk_level in risk_counts: risk_counts[s.risk_level] += 1
        elif s.risk_level == 'Extremely Severe': risk_counts['Severe'] += 1 
        elif not s.risk_level: risk_counts['Normal'] += 1 # Default to normal if none
        
    # 2. Chart Data - Cohort Mean Scores
    cohort_list = ["Batch 2022", "Batch 2023", "Batch 2024", "Batch 2025"]
    domain_overview_by_cohort = {}
    
    # Initialize overall averages accumulator
    overall_sums = {
        'Stress': [], 'Anxiety': [], 'Depression': [],
        'Impulsivity': [], 'Non-Planning': [], 'Risk-Taking': [], 'Aggression': []
    }
    
    for ch in cohort_list:
        # Filter students in this cohort
        ch_students = [s for s in assigned_students if (f"Batch {2025 - s.year_of_study + 1}" if s.year_of_study else "Batch 2025") == ch]
        ch_student_ids = [s.id for s in ch_students]
        
        # Get completed sessions for this cohort
        ch_sessions = AssessmentSession.query.filter(
            AssessmentSession.student_id.in_(ch_student_ids),
            AssessmentSession.status == 'completed'
        ).all()
        ch_session_ids = [sess.id for sess in ch_sessions]
        
        # Query all scores for these sessions
        scores = AssessmentScore.query.filter(AssessmentScore.session_id.in_(ch_session_ids)).all()
        
        # Group scores by session
        session_scores = {}
        for sc in scores:
            if sc.session_id not in session_scores:
                session_scores[sc.session_id] = {}
            session_scores[sc.session_id][sc.assessment.name] = sc
            
        # Accumulate domains
        ch_sums = {
            'Stress': [], 'Anxiety': [], 'Depression': [],
            'Impulsivity': [], 'Non-Planning': [], 'Risk-Taking': [], 'Aggression': []
        }
        
        for sess_id, ass_scores in session_scores.items():
            # DASS-21
            dass_sc = ass_scores.get('DASS-21')
            if dass_sc and dass_sc.category_scores:
                cs = dass_sc.category_scores
                # Handle old vs new nested structure
                if "category_scores" in cs:
                    dep = cs["category_scores"].get("Depression", 0)
                    anx = cs["category_scores"].get("Anxiety", 0)
                    st = cs["category_scores"].get("Stress", 0)
                else:
                    dep = cs.get('depression', {}).get('score', 0)
                    anx = cs.get('anxiety', {}).get('score', 0)
                    st = cs.get('stress', {}).get('score', 0)
                
                ch_sums['Stress'].append(st / 14.0)
                ch_sums['Anxiety'].append(anx / 14.0)
                ch_sums['Depression'].append(dep / 14.0)
                
            # BFI-44
            bfi_sc = ass_scores.get('BFI-44')
            if bfi_sc and bfi_sc.category_scores:
                cs = bfi_sc.category_scores
                if "category_scores" in cs:
                    neuro = cs["category_scores"].get("Neuroticism", 3.0)
                    consc = cs["category_scores"].get("Conscientiousness", 3.0)
                    agree = cs["category_scores"].get("Agreeableness", 3.0)
                else:
                    neuro = cs.get('neuroticism', {}).get('score', 3.0)
                    consc = cs.get('conscientiousness', {}).get('score', 3.0)
                    agree = cs.get('agreeableness', {}).get('score', 3.0)
                    
                ch_sums['Impulsivity'].append((neuro - 1.0) * 0.75)
                ch_sums['Non-Planning'].append((5.0 - consc) * 0.75)
                ch_sums['Aggression'].append((5.0 - agree) * 0.75)
                
            # Home Adjustment Questionnaire for Risk-Taking
            home_sc = ass_scores.get('Home Adjustment Questionnaire')
            if home_sc:
                h_score = home_sc.total_score or 0
                ch_sums['Risk-Taking'].append(h_score / 5.0)
                
        # Compute averages for this cohort
        cohort_chart_data = []
        for name in ['Stress', 'Anxiety', 'Depression', 'Impulsivity', 'Non-Planning', 'Risk-Taking', 'Aggression']:
            vals = ch_sums[name]
            avg_val = round(sum(vals) / len(vals), 2) if vals else 1.5 # default to 1.5 if no data
            
            # Map into Recharts data format
            dass_val = avg_val if name in ['Stress', 'Anxiety', 'Depression'] else None
            bis_val = avg_val if name in ['Impulsivity', 'Non-Planning'] else None
            risk_val = avg_val if name in ['Risk-Taking', 'Aggression'] else None
            
            cohort_chart_data.append({
                "name": name,
                "DASS-21": dass_val,
                "BIS-11": bis_val,
                "Behavioural Risk": risk_val
            })
            
            # Accumulate for overall
            overall_sums[name].extend(vals)
            
        domain_overview_by_cohort[ch] = cohort_chart_data
        
    # Also calculate the overall/All averages
    overall_chart_data = []
    for name in ['Stress', 'Anxiety', 'Depression', 'Impulsivity', 'Non-Planning', 'Risk-Taking', 'Aggression']:
        vals = overall_sums[name]
        avg_val = round(sum(vals) / len(vals), 2) if vals else 1.5
        
        dass_val = avg_val if name in ['Stress', 'Anxiety', 'Depression'] else None
        bis_val = avg_val if name in ['Impulsivity', 'Non-Planning'] else None
        risk_val = avg_val if name in ['Risk-Taking', 'Aggression'] else None
        
        overall_chart_data.append({
            "name": name,
            "DASS-21": dass_val,
            "BIS-11": bis_val,
            "Behavioural Risk": risk_val
        })
        
    domain_overview_by_cohort["All"] = overall_chart_data
    domain_overview_by_cohort["All Cohorts"] = overall_chart_data

    total_students = len(assigned_students)
    chart_data = {
        'overall_risk': {
            'labels': ['Low Risk', 'Moderate Risk', 'High Risk', 'Severe Risk'],
            'data': [risk_counts['Normal'], risk_counts['Mild'], risk_counts['Moderate'], risk_counts['Severe']],
            'percentages': [f"{(risk_counts['Normal']/total_students*100 if total_students else 0):.1f}%", 
                            f"{(risk_counts['Mild']/total_students*100 if total_students else 0):.1f}%", 
                            f"{(risk_counts['Moderate']/total_students*100 if total_students else 0):.1f}%", 
                            f"{(risk_counts['Severe']/total_students*100 if total_students else 0):.1f}%"]
        },
        'domain_overview': {
            'labels': ['Stress', 'Anxiety', 'Depression', 'Impulsivity', 'Non-Planning\nImpulsivity', 'Risk-Taking', 'Aggression'],
            'data': [1.85, 1.62, 1.39, 2.11, 2.32, 1.78, 1.46] # Mocked domain averages kept for legacy fallback
        },
        'domain_overview_by_cohort': domain_overview_by_cohort,
        'cohort_risk': {
            'labels': ['Batch 2022\n(n=120)', 'Batch 2023\n(n=118)', 'Batch 2024\n(n=122)', 'Batch 2025\n(n=126)'],
            'low': [56, 52, 50, 55],
            'moderate': [24, 27, 26, 25],
            'high': [13, 14, 15, 13],
            'severe': [7, 7, 9, 6]
        },
        'trend': {
            'labels': ['Dec \'24', 'Jan \'25', 'Feb \'25', 'Mar \'25', 'Apr \'25', 'May \'25'],
            'data': [14, 16, 18, 21, 23, 27]
        }
    }

    # 3. Students Table
    flagged_students_list = []
    attention_students = StudentProfile.query.filter(
        StudentProfile.id.in_(student_ids),
        or_(StudentProfile.risk_level == 'Moderate', StudentProfile.risk_level == 'Severe', StudentProfile.risk_level == 'Extremely Severe')
    ).all()
    
    for student in attention_students:
        has_flag = Flag.query.filter_by(student_id=student.user_id, is_resolved=False).first()
        
        dass_severity = student.risk_level
        impulsivity_level = "Moderate"
        risk_level = "High"
        student_scores = [s for s in scores if s.session.student_id == student.id]
        for s in student_scores:
            if s.assessment.name == 'BFI-44':
                impulsivity_level = s.category_scores.get('neuroticism', {}).get('level', 'Moderate')
            elif s.assessment.name == 'EQ':
                risk_level = s.severity_label
                
        flagged_students_list.append({
            "profile_id": student.id,
            "name": student.user.name,
            "id": student.user.uai_id,
            "course": student.course or "B.Sc. Agriculture",
            "cohort": f"Batch {2025 - student.year_of_study + 1}" if student.year_of_study else "Batch 2025",
            "stress": dass_severity,
            "impulsivity": impulsivity_level,
            "risk_taking": risk_level,
            "flag": "Yes" if has_flag else "No"
        })

    return render_template('counsellor/dashboard.html', 
                           kpis=kpis, 
                           chart_data=chart_data, 
                           flagged_students=flagged_students_list)

@counsellor.route('/student/<int:student_id>/report', methods=['GET'])
@login_required
@role_required('counsellor')
def student_report_page(student_id):
    student = StudentProfile.query.get_or_404(student_id)
    return render_template('counsellor/student_report.html', student=student)

@counsellor.route('/student/<int:student_id>/pdf', methods=['GET'])
@login_required
@role_required('counsellor')
def export_student(student_id):
    profile = StudentProfile.query.get_or_404(student_id)
    
    # Verify counsellor is assigned to this student
    if profile.assigned_counsellor_id != current_user.id:
        return jsonify({"error": "Unauthorized. This student is not assigned to you."}), 403
        
    try:
        from utils.pdf_generator import generate_student_pdf
        pdf_buffer = generate_student_pdf(student_id)
        
        student_name = profile.user.name.replace(" ", "_")
        session_obj = AssessmentSession.query.filter_by(student_id=profile.id, status='completed').order_by(AssessmentSession.completed_at.desc()).first()
        date_str = session_obj.completed_at.strftime('%Y-%m-%d') if (session_obj and session_obj.completed_at) else datetime.utcnow().strftime('%Y-%m-%d')
        filename = f"SafeSpace_Report_{student_name}_{date_str}.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@counsellor.route('/api/counsellor/student/<int:student_id>/report/pdf', methods=['GET'])
@login_required
@role_required('counsellor')
def api_student_report_pdf(student_id):
    profile = StudentProfile.query.get_or_404(student_id)
    
    # Verify counsellor is assigned to this student
    if profile.assigned_counsellor_id != current_user.id:
        return jsonify({"error": "Unauthorized. This student is not assigned to you."}), 403
        
    try:
        from utils.pdf_generator import generate_student_pdf
        pdf_buffer = generate_student_pdf(student_id)
        
        student_name = profile.user.name.replace(" ", "_")
        session_obj = AssessmentSession.query.filter_by(student_id=profile.id, status='completed').order_by(AssessmentSession.completed_at.desc()).first()
        date_str = session_obj.completed_at.strftime('%Y-%m-%d') if (session_obj and session_obj.completed_at) else datetime.utcnow().strftime('%Y-%m-%d')
        filename = f"SafeSpace_Report_{student_name}_{date_str}.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@counsellor.route('/api/counsellor/student/<int:student_id>/report', methods=['GET'])
@login_required
@role_required('counsellor')
def api_student_report(student_id):
    profile = StudentProfile.query.get_or_404(student_id)
    user = profile.user
    
    # Get the latest completed session
    session_obj = AssessmentSession.query.filter_by(student_id=profile.id, status='completed').order_by(AssessmentSession.completed_at.desc()).first()
    
    if not session_obj:
        return jsonify({"error": "No completed assessment session found for this student."}), 404
        
    # Query scores
    scores = AssessmentScore.query.filter_by(session_id=session_obj.id).all()
    scores_by_assessment = {s.assessment.name: s for s in scores}
    
    # Format DASS-21
    dass_data = {}
    dass_score = scores_by_assessment.get("DASS-21")
    if dass_score:
        dass_data = dass_score.category_scores
        
    # Format BFI-44
    bfi_data = {}
    bfi_score = scores_by_assessment.get("BFI-44")
    if bfi_score:
        bfi_data = bfi_score.category_scores
        
    # Format EQ
    eq_data = {}
    eq_score = scores_by_assessment.get("EQ")
    if eq_score:
        eq_data = eq_score.category_scores
        
    # Format SQ
    sq_data = {}
    sq_score = scores_by_assessment.get("SQ")
    if sq_score:
        sq_data = sq_score.category_scores
        
    # Format HOME
    home_data = {}
    home_score = scores_by_assessment.get("Home Adjustment Questionnaire")
    if home_score:
        home_data = home_score.category_scores
        
    # Get all responses for response time graph
    responses = Response.query.filter_by(session_id=session_obj.id).join(Question).order_by(Question.assessment_id, Question.order_number).all()
    
    response_times = []
    skipped_flags = []
    question_labels = []
    
    total_answered = 0
    auto_skipped = 0
    total_time = 0
    
    for idx, r in enumerate(responses):
        t = r.time_taken_seconds or 0
        response_times.append(t)
        skipped_flags.append(r.auto_submitted)
        question_labels.append(idx + 1)
        
        if r.selected_option is not None and not r.auto_submitted:
            total_answered += 1
        if r.auto_submitted:
            auto_skipped += 1
        total_time += t
        
    avg_time = round(total_time / len(responses), 1) if responses else 0
    
    # Re-calculate overall risk and recommendations using utils.scoring
    from utils.scoring import determine_overall_risk
    
    all_scores_structured = {
        "DASS21": dass_data,
        "BFI44": bfi_data,
        "EQ": {
            "total_score": eq_score.total_score if eq_score else 30
        },
        "SQ": {
            "total_score": sq_score.total_score if sq_score else 30
        },
        "HOME": {
            "total_score": home_score.total_score if home_score else 0
        }
    }
    
    risk_data = determine_overall_risk(all_scores_structured)

    # Fetch all questions and responses in order
    all_questions = Question.query.join(Assessment).order_by(Assessment.id, Question.order_number).all()
    all_responses = Response.query.filter_by(session_id=session_obj.id).all()
    resp_map_all = {r.question_id: r for r in all_responses}
    
    question_responses = []
    for idx, q in enumerate(all_questions):
        r = resp_map_all.get(q.id)
        selected_val = "—"
        selected_lbl = "—"
        if r and r.selected_option is not None:
            selected_val = r.selected_option
            for opt in (q.options or []):
                if str(opt.get('value')) == str(r.selected_option):
                    selected_lbl = opt.get('label', r.selected_option)
                    break
            else:
                selected_lbl = r.selected_option
                
        sec_name = "Other"
        if q.assessment.name == "DASS-21":
            sec_name = "Section 1 (DASS-21)"
        elif q.assessment.name == "BFI-44":
            sec_name = "Section 2 (BFI-44)"
        elif q.assessment.name == "EQ":
            sec_name = "Section 3 (EQ)"
        elif q.assessment.name == "SQ":
            sec_name = "Section 4 (SQ)"
        elif q.assessment.name == "UAI Psychology Quiz":
            sec_name = "Section 5 (UAI Quiz)"
        elif q.assessment.name == "Home Adjustment Questionnaire":
            sec_name = "Section 6 (Home Adjustment)"
            
        question_responses.append({
            "num": idx + 1,
            "section": sec_name,
            "category": q.category,
            "text": q.question_text,
            "value": selected_val,
            "label": selected_lbl
        })
    
    report_payload = {
        "student": {
            "name": user.name,
            "uai_id": user.uai_id,
            "department": profile.department or "Psychology",
            "year": profile.year_of_study or 1,
            "age": profile.age,
            "gender": profile.gender,
            "risk_level": risk_data["risk_level"].upper()
        },
        "dass21": dass_data,
        "bfi44": bfi_data,
        "eq": eq_data,
        "sq": sq_data,
        "home": home_data,
        "time_behavior": {
            "question_numbers": question_labels,
            "times": response_times,
            "skipped": skipped_flags,
            "stats": {
                "total_answered": total_answered,
                "auto_skipped": auto_skipped,
                "avg_time": avg_time
            }
        },
        "risk_assessment": risk_data,
        "question_responses": question_responses
    }
    
    return jsonify(report_payload)

@counsellor.route('/api/counsellor/student/<int:student_id>/full-report', methods=['GET'])
@login_required
@role_required('counsellor')
def api_student_full_report(student_id):
    profile = StudentProfile.query.get_or_404(student_id)
    user = profile.user
    
    # Verify counsellor is assigned to this student
    if profile.assigned_counsellor_id != current_user.id:
        return jsonify({"error": "Unauthorized. This student is not assigned to you."}), 403
    
    session_obj = AssessmentSession.query.filter_by(student_id=profile.id, status='completed').order_by(AssessmentSession.completed_at.desc()).first()
    if not session_obj:
        return jsonify({"error": "No completed assessment session found."}), 404
        
    scores = AssessmentScore.query.filter_by(session_id=session_obj.id).all()
    scores_by_assessment = {s.assessment.name: s for s in scores}
    
    from utils.report_text_generator import (
        generate_bfi_interpretation,
        generate_dass_interpretation,
        generate_dass_overall,
        generate_eq_sq_interpretation,
        generate_home_adjustment_interpretation,
        generate_integrated_summary
    )
    
    # 1. BFI-44
    bfi_sc = scores_by_assessment.get("BFI-44")
    bfi_data = {}
    if bfi_sc and bfi_sc.category_scores:
        cs = bfi_sc.category_scores
        bfi_scores = cs.get("category_scores", {})
        bfi_labels = cs.get("severity_labels", {})
        
        # Openness normalization
        opn_lvl = bfi_labels.get("Openness to Experience") or bfi_labels.get("Openness", "Moderate")
        bfi_labels["Openness"] = opn_lvl
        
        bfi_data = {
            "scores": { d: {"score": float(bfi_scores.get(d, 3.0)), "level": bfi_labels.get(d, "Moderate")} for d in ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"] },
            "interpretations": { d: generate_bfi_interpretation(d, bfi_labels.get(d, "Moderate")) for d in ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"] },
            "overall_paragraph": "The personality profile suggests that the student's behavioural style, emotional functioning, and interpersonal tendencies are shaped by the above personality characteristics. These traits may influence academic adjustment, peer relationships, coping styles, and response to challenges.",
            "levels": bfi_labels,
            "overall": "The personality profile suggests that the student's behavioural style, emotional functioning, and interpersonal tendencies are shaped by the above personality characteristics. These traits may influence academic adjustment, peer relationships, coping styles, and response to challenges."
        }
        
    # 2. DASS-21
    dass_sc = scores_by_assessment.get("DASS-21")
    dass_data = {}
    if dass_sc and dass_sc.category_scores:
        cs = dass_sc.category_scores
        dass_scores = cs.get("category_scores", {})
        dass_labels = cs.get("severity_labels", {})
        
        dass_data = {
            "scores": { s: {"score": int(dass_scores.get(s, 0)), "severity": dass_labels.get(s, "Normal")} for s in ["Depression", "Anxiety", "Stress"] },
            "interpretations": { s: generate_dass_interpretation(s, dass_labels.get(s, "Normal")) for s in ["Depression", "Anxiety", "Stress"] },
            "overall_paragraph": generate_dass_overall(dass_labels),
            "levels": dass_labels,
            "overall": generate_dass_overall(dass_labels)
        }
        
    # 3. EQ-SQ
    eq_sc = scores_by_assessment.get("EQ")
    sq_sc = scores_by_assessment.get("SQ")
    
    eq_score_val = int(eq_sc.total_score) if eq_sc else 20
    sq_score_val = int(sq_sc.total_score) if sq_sc else 20
    
    eq_lvl = eq_sc.category_scores.get("severity_labels", {}).get("Emotional Awareness", "Moderate") if eq_sc else "Moderate"
    sq_lvl = sq_sc.category_scores.get("severity_labels", {}).get("Social Awareness", "Moderate") if sq_sc else "Moderate"
    
    eq_p, sq_p, overall_eq_sq_p = generate_eq_sq_interpretation(eq_lvl, sq_lvl)
    
    eq_sq_data = {
        "scores": {
            "EQ": {"score": eq_score_val, "level": eq_lvl},
            "SQ": {"score": sq_score_val, "level": sq_lvl}
        },
        "interpretations": {
            "EQ": eq_p,
            "SQ": sq_p
        },
        "overall_paragraph": overall_eq_sq_p,
        "eq_score": eq_score_val,
        "eq_level": eq_lvl,
        "sq_score": sq_score_val,
        "sq_level": sq_lvl,
        "eq_interpretation": eq_p,
        "sq_interpretation": sq_p,
        "overall": overall_eq_sq_p
    }
    
    # 4. Home Adjustment
    home_sc = scores_by_assessment.get("Home Adjustment Questionnaire")
    home_score_val = int(home_sc.total_score) if home_sc else 0
    
    if home_score_val <= 4:
        home_lvl = "Healthy Adjustment"
        home_color = "green"
    elif home_score_val <= 9:
        home_lvl = "Mild Concerns"
        home_color = "yellow"
    else:
        home_lvl = "Significant Difficulties"
        home_color = "red"
        
    home_adjustment_data = {
        "score": home_score_val,
        "level": home_lvl,
        "color": home_color,
        "interpretation": generate_home_adjustment_interpretation(home_lvl)
    }
    
    # 5. Integrated Summary
    summary_data = {
        "bfi": {"levels": {d: bfi_data["scores"][d]["level"] for d in bfi_data["scores"]}} if bfi_data else {},
        "dass": {"levels": {s: dass_data["scores"][s]["severity"] for s in dass_data["scores"]}} if dass_data else {},
        "eq_sq": {"eq_level": eq_lvl, "sq_level": sq_lvl},
        "home": {"level": home_lvl}
    }
    
    integrated_summary = generate_integrated_summary(summary_data)
    
    payload = {
        "student": {
            "name": user.name,
            "age": profile.age,
            "gender": profile.gender.capitalize() if profile.gender else "N/A",
            "admission_number": user.uai_id,
            "cohort": f"Batch {2025 - profile.year_of_study + 1}" if profile.year_of_study else "Batch 2025",
            "date_of_assessment": session_obj.completed_at.strftime('%Y-%m-%d') if session_obj.completed_at else "N/A",
            "uai_id": user.uai_id,
            "date": session_obj.completed_at.strftime('%Y-%m-%d') if session_obj.completed_at else "N/A"
        },
        "bfi44": bfi_data,
        "dass21": dass_data,
        "eq_sq": eq_sq_data,
        "home_adjustment": home_adjustment_data,
        "home": home_adjustment_data,
        "integrated_summary": integrated_summary,
        "summary": integrated_summary
    }
    
    return jsonify(payload)
