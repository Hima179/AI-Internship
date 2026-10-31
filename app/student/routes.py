from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from . import student
from ..auth import role_required
from ..models import StudentProfile, AssessmentSession, Question, Response, Assessment, AssessmentScore, db
from ..scoring import run_all_scores

@student.route('/consent', methods=['GET', 'POST'])
@login_required
@role_required('student')
def consent():
    profile = current_user.student_profile
    if profile and profile.consent_given:
        if profile.age and profile.department:
            return redirect(url_for('student.dashboard'))
        return redirect(url_for('student.details'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'agree':
            if not profile:
                profile = StudentProfile(user_id=current_user.id)
                db.session.add(profile)
            
            profile.consent_given = True
            profile.consent_timestamp = datetime.utcnow()
            db.session.commit()
            
            flash('Consent recorded successfully.', 'success')
            return redirect(url_for('student.details'))
        elif action == 'decline':
            flash('You must consent to proceed with the assessment.', 'warning')
            
    return render_template('student/consent.html', title='Informed Consent')

from .forms import StudentDetailsForm

@student.route('/details', methods=['GET', 'POST'])
@login_required
@role_required('student')
def details():
    profile = current_user.student_profile
    if not profile or not profile.consent_given:
        return redirect(url_for('student.consent'))
    
    if profile.age and profile.department:
        latest = AssessmentSession.query.filter_by(student_id=profile.id, status='completed').first()
        if latest:
            return redirect(url_for('student.dashboard'))
    
    form = StudentDetailsForm()
    
    if form.validate_on_submit():
        current_user.name = form.name.data
        profile.age = form.age.data
        profile.gender = form.gender.data
        profile.department = form.department.data
        profile.year_of_study = form.year_of_study.data
        profile.phone = form.phone.data
        profile.previous_counselling = form.previous_counselling.data
        profile.mental_health_diagnosis = form.mental_health_diagnosis.data
        db.session.commit()
        flash('Details updated successfully.', 'success')
        return redirect(url_for('student.instructions'))
    
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.age.data = profile.age
        form.gender.data = profile.gender
        form.department.data = profile.department
        form.year_of_study.data = profile.year_of_study
        form.phone.data = profile.phone
        form.previous_counselling.data = profile.previous_counselling
        form.mental_health_diagnosis.data = profile.mental_health_diagnosis
        
    return render_template('student/details.html', title='Student Details', form=form)

@student.route('/instructions')
@login_required
@role_required('student')
def instructions():
    profile = current_user.student_profile
    if not profile or not profile.consent_given:
        return redirect(url_for('student.consent'))
    if not profile.age or not profile.department:
        return redirect(url_for('student.details'))
    return render_template('student/instructions.html', title='Assessment Instructions')

@student.route('/assessment/start')
@login_required
@role_required('student')
def assessment_start():
    profile = current_user.student_profile
    if not profile or not profile.consent_given:
        return redirect(url_for('student.consent'))
    if not profile.age or not profile.department:
        return redirect(url_for('student.details'))
        
    # Redirect to dashboard if already completed
    latest = AssessmentSession.query.filter_by(student_id=profile.id, status='completed').first()
    if latest:
        return redirect(url_for('student.dashboard'))
        
    # Create new session
    new_session = AssessmentSession(
        student_id=profile.id,
        started_at=datetime.utcnow(),
        status='in_progress'
    )
    db.session.add(new_session)
    db.session.commit()
    session['assessment_session_id'] = new_session.id
    session['acknowledged_sections'] = []
    return redirect(url_for('student.assessment_question', q_num=1))

@student.route('/assessment/question/<int:q_num>')
@login_required
@role_required('student')
def assessment_question(q_num):
    sess_id = session.get('assessment_session_id')
    if not sess_id:
        return redirect(url_for('student.instructions'))
    
    # Fetch all questions ordered by assessment and order_number
    questions = Question.query.join(Assessment).order_by(Assessment.id, Question.order_number).all()
    total = len(questions)
    if q_num < 1 or q_num > total:
        return redirect(url_for('student.assessment_question', q_num=1))

    # Fetch all responses to see what has been answered
    responses = Response.query.filter_by(session_id=sess_id).all()

    question = questions[q_num - 1]
    assessment_name = question.assessment.name

    # Check if section instructions need to be displayed
    is_section_start = False
    if q_num == 1:
        is_section_start = True
    else:
        prev_question = questions[q_num - 2]
        if question.assessment_id != prev_question.assessment_id:
            is_section_start = True
            
    if is_section_start:
        acknowledged = session.get('acknowledged_sections', [])
        if question.assessment_id not in acknowledged:
            return redirect(url_for('student.section_instructions', assessment_id=question.assessment_id, next_q_num=q_num))

    # Rename assessment name for display to student (hide actual names)
    SECTION_NAME_MAP = {
        "DASS-21": "Section 1",
        "BFI-44": "Section 2",
        "EQ": "Section 3",
        "SQ": "Section 4",
        "UAI Psychology Quiz": "Section 5",
        "Home Adjustment Questionnaire": "Section 6"
    }
    display_assessment_name = SECTION_NAME_MAP.get(assessment_name, assessment_name)

    # Build a map of question_id -> status for the navigator
    responded_map = {}
    for r in responses:
        if r.auto_submitted and r.selected_option is None:
            responded_map[r.question_id] = 'expired'
        else:
            responded_map[r.question_id] = 'attempted'

    # Build list of (q_num, question_id, status) for navigator
    nav_questions = []
    for idx, q in enumerate(questions):
        status = responded_map.get(q.id, 'unattempted')
        nav_questions.append({'num': idx + 1, 'id': q.id, 'status': status})

    return render_template('student/question.html', 
                           question=question, 
                           q_num=q_num, 
                           total=total, 
                           session_id=sess_id, 
                           assessment_name=display_assessment_name,
                           nav_questions=nav_questions)

@student.route('/assessment/instructions/<int:assessment_id>')
@login_required
@role_required('student')
def section_instructions(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    next_q_num = request.args.get('next_q_num', type=int)
    if not next_q_num:
        return redirect(url_for('student.dashboard'))
        
    q_count = Question.query.filter_by(assessment_id=assessment_id).count()

    SECTION_DETAILS = {
        "DASS-21": {
            "title": "Section 1: Well-being Indicators",
            "subtitle": "Depression, Anxiety and Stress Scale (DASS-21)",
            "icon": "fa-solid fa-heart-pulse",
            "color": "#e11d48",
            "points": [
                "This section contains 21 statements about your recent emotional states.",
                "Read each statement and select the option (Never, Sometimes, Often, Almost Always) that indicates how much the statement applied to you over the past week.",
                "Do not spend too much time on any one statement; your first reaction is usually the most accurate.",
                "All questions are compulsory."
            ]
        },
        "BFI-44": {
            "title": "Section 2: Personality Profile",
            "subtitle": "Big Five Inventory (BFI-44)",
            "icon": "fa-solid fa-user-check",
            "color": "#0284c7",
            "points": [
                "This section contains 44 short statements describing various personality traits.",
                "For each statement, indicate the extent to which you agree or disagree using the 5-point scale (Disagree Strongly to Agree Strongly).",
                "Answer based on how you actually see yourself, not how you wish to be in the future.",
                "All statements begin with 'I see myself as someone who...'",
                "All questions are compulsory."
            ]
        },
        "EQ": {
            "title": "Section 3: Empathy Assessment",
            "subtitle": "Empathy Quotient (EQ)",
            "icon": "fa-solid fa-face-smile",
            "color": "#0d9488",
            "points": [
                "This section contains 8 statements regarding your interpersonal awareness and empathy.",
                "Please indicate how strongly you agree or disagree with each statement.",
                "Be as honest as possible. There are no right or wrong answers.",
                "All questions are compulsory."
            ]
        },
        "SQ": {
            "title": "Section 4: Systemizing Assessment",
            "subtitle": "Systemizing Quotient (SQ)",
            "icon": "fa-solid fa-gears",
            "color": "#4f46e5",
            "points": [
                "This section contains 8 statements about your interest in systems, rules, and structures.",
                "Please indicate how strongly you agree or disagree with each statement.",
                "Choose the options that reflect your true interest or daily habits.",
                "All questions are compulsory."
            ]
        },
        "UAI Psychology Quiz": {
            "title": "Section 5: General Aptitude & Logic",
            "subtitle": "Universal AI Psychology Quiz",
            "icon": "fa-solid fa-lightbulb",
            "color": "#ca8a04",
            "points": [
                "This section contains 200 multiple-choice questions assessing various cognitive and psychological concepts.",
                "For each question, select the best answer from the options provided.",
                "Take your time to understand the question before selecting.",
                "All questions are compulsory."
            ]
        },
        "Home Adjustment Questionnaire": {
            "title": "Section 6: Home & Family Adjustment",
            "subtitle": "Home Adjustment Questionnaire",
            "icon": "fa-solid fa-house-chimney-user",
            "color": "#2563eb",
            "points": [
                "This section contains 15 questions about your home environment and family dynamics.",
                "For each statement, select whether it is 'True' or 'Not True' for you.",
                "Answer based on your current living situation and family relationships.",
                "All questions are compulsory."
            ]
        }
    }

    details = SECTION_DETAILS.get(assessment.name, {
        "title": f"Section: {assessment.name}",
        "subtitle": assessment.description or "",
        "icon": "fa-solid fa-file-invoice",
        "color": "#475569",
        "points": [
            f"This section has {q_count} questions.",
            "Please read each statement carefully.",
            "All questions are compulsory."
        ]
    })

    return render_template('student/section_instructions.html',
                           assessment=assessment,
                           next_q_num=next_q_num,
                           details=details)

@student.route('/assessment/acknowledge/<int:assessment_id>')
@login_required
@role_required('student')
def acknowledge_instructions(assessment_id):
    next_q_num = request.args.get('next_q_num', type=int)
    if not next_q_num:
        return redirect(url_for('student.dashboard'))
        
    acknowledged = session.get('acknowledged_sections', [])
    if assessment_id not in acknowledged:
        acknowledged.append(assessment_id)
        session['acknowledged_sections'] = acknowledged
        
    return redirect(url_for('student.assessment_question', q_num=next_q_num))

@student.route('/assessment/answer', methods=['POST'])
@login_required
@role_required('student')
def assessment_answer():
    data = request.get_json()
    q_id = data.get('question_id')
    selected = data.get('selected_option')
    time_taken = data.get('time_taken')
    auto = data.get('auto_submitted', False)
    sess_id = session.get('assessment_session_id')
    
    if not sess_id:
        return jsonify({'success': False, 'message': 'No active session'}), 400
    
    # Check if response already exists for this question in this session
    resp = Response.query.filter_by(session_id=sess_id, question_id=q_id).first()
    if resp:
        resp.selected_option = selected
        resp.time_taken_seconds = time_taken
        resp.auto_submitted = auto
    else:
        resp = Response(
            session_id=sess_id,
            question_id=q_id,
            selected_option=selected,
            time_taken_seconds=time_taken,
            auto_submitted=auto
        )
        db.session.add(resp)
    
    db.session.commit()
    
    # Get total questions to check if it's the last
    total = Question.query.count()
    q_num = int(request.args.get('q_num', 0)) # We'll pass q_num in JS
    
    return jsonify({
        'success': True, 
        'next_question': q_num + 1, 
        'is_last': q_num >= total
    })

@student.route('/assessment/complete', methods=['POST'])
@login_required
@role_required('student')
def assessment_complete():
    data = request.get_json()
    sess_id = data.get('session_id') or session.get('assessment_session_id')
    total_time = data.get('total_time')
    
    sess = AssessmentSession.query.get(sess_id)
    if sess:
        sess.completed_at = datetime.utcnow()
        sess.status = 'completed'
        sess.total_time_seconds = total_time
        db.session.commit()
        
        # Trigger scoring
        run_all_scores(sess_id)
        
        session.pop('assessment_session_id', None)
        return jsonify({'success': True, 'redirect': url_for('student.complete')})
    
    return jsonify({'success': False}), 400

@student.route('/complete')
@login_required
@role_required('student')
def complete():
    import json, os
    from datetime import timezone

    profile = current_user.student_profile
    latest = AssessmentSession.query.filter_by(
        student_id=profile.id, status='completed'
    ).order_by(AssessmentSession.completed_at.desc()).first()

    if not latest:
        return redirect(url_for('student.dashboard'))

    # Get all questions in order
    questions = Question.query.join(Assessment).order_by(Assessment.id, Question.order_number).all()
    total_questions = len(questions)

    # Get all responses for this session mapped by question_id
    responses = Response.query.filter_by(session_id=latest.id).all()
    resp_map = {r.question_id: r for r in responses}

    # Build per-question detail rows + compute stats
    correct = wrong = expired = unattempted = 0
    total_time_answered = 0
    answered_times = []   # list of (q_num, time_taken)
    table_rows = []

    for idx, q in enumerate(questions):
        q_num = idx + 1
        r = resp_map.get(q.id)
        selected_label = '—'
        status = 'unattempted'
        time_taken = None

        if r:
            time_taken = r.time_taken_seconds or 0
            if r.auto_submitted and r.selected_option is None:
                status = 'expired'
                expired += 1
                selected_label = '— (Time Up)'
            elif r.selected_option is not None:
                # Find the label for the selected value
                for opt in (q.options or []):
                    if str(opt.get('value')) == str(r.selected_option):
                        selected_label = opt.get('label', r.selected_option)
                        break
                else:
                    selected_label = r.selected_option

                # Check if correct (UAI quiz stores answer as letter like "A", "B" etc.)
                # For UAI quiz, the correct answer isn't stored in DB — we track attempted only
                status = 'attempted'
                answered_times.append((q_num, time_taken))
                total_time_answered += time_taken

        table_rows.append({
            'q_num': q_num,
            'question_short': (q.question_text[:70] + '…') if len(q.question_text) > 70 else q.question_text,
            'your_answer': selected_label,
            'time_taken': time_taken,
            'status': status,
        })

    attempted = len(answered_times) + expired
    unattempted = total_questions - attempted

    avg_time = round(total_time_answered / len(answered_times), 1) if answered_times else 0
    fastest = min(answered_times, key=lambda x: x[1]) if answered_times else None
    slowest = max(answered_times, key=lambda x: x[1]) if answered_times else None

    total_sess_secs = latest.total_time_seconds or 0
    total_time_fmt = f"{total_sess_secs // 60:02d}:{total_sess_secs % 60:02d}"

    stats = {
        'total': total_questions,
        'attempted': attempted,
        'expired': expired,
        'unattempted': unattempted,
        'score': attempted,   # 1 point per attempted (not graded since no answer key in DB)
        'avg_time': avg_time,
        'fastest': fastest,
        'slowest': slowest,
        'total_time': total_time_fmt,
        'completed_at': latest.completed_at.strftime('%Y-%m-%d %H:%M:%S') if latest.completed_at else '—',
    }

    # Save session_log.json
    results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'results')
    os.makedirs(results_dir, exist_ok=True)
    log_path = os.path.join(results_dir, 'session_log.json')

    log_entry = {
        'timestamp': latest.completed_at.strftime('%Y-%m-%d %H:%M:%S') if latest.completed_at else '',
        'student': current_user.name,
        'uai_id': current_user.uai_id,
        'session_id': latest.id,
        'stats': stats,
        'questions': table_rows,
    }

    # Load existing logs or start fresh
    existing = []
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r') as f:
                existing = json.load(f)
        except Exception:
            existing = []

    existing.append(log_entry)
    with open(log_path, 'w') as f:
        json.dump(existing, f, indent=2, default=str)

    # Store session_id in flask session for export
    session['export_session_id'] = latest.id

    return render_template('student/complete.html',
                           stats=stats,
                           table_rows=table_rows,
                           student_name=current_user.name)


@student.route('/export_results')
@login_required
@role_required('student')
def export_results():
    import os
    from flask import make_response

    profile = current_user.student_profile
    latest = AssessmentSession.query.filter_by(
        student_id=profile.id, status='completed'
    ).order_by(AssessmentSession.completed_at.desc()).first()

    if not latest:
        return redirect(url_for('student.dashboard'))

    questions = Question.query.join(Assessment).order_by(Assessment.id, Question.order_number).all()
    responses = Response.query.filter_by(session_id=latest.id).all()
    resp_map = {r.question_id: r for r in responses}

    lines = []
    lines.append("=" * 60)
    lines.append("       UNIVERSAL AI UNIVERSITY — QUIZ RESULTS REPORT")
    lines.append("=" * 60)
    lines.append(f"Student   : {current_user.name} ({current_user.uai_id})")
    lines.append(f"Date      : {latest.completed_at.strftime('%Y-%m-%d %H:%M:%S') if latest.completed_at else '—'}")
    lines.append(f"Session ID: {latest.id}")
    lines.append("-" * 60)

    attempted = expired = 0
    answered_times = []
    row_lines = []

    for idx, q in enumerate(questions):
        q_num = idx + 1
        r = resp_map.get(q.id)
        ans = '—'
        status = 'Not Attempted'
        t = '—'
        if r:
            t = f"{r.time_taken_seconds}s" if r.time_taken_seconds is not None else '—'
            if r.auto_submitted and r.selected_option is None:
                status = 'Expired'
                expired += 1
                ans = '(Time Up)'
            elif r.selected_option is not None:
                attempted += 1
                status = 'Attempted'
                for opt in (q.options or []):
                    if str(opt.get('value')) == str(r.selected_option):
                        ans = opt.get('label', r.selected_option)
                        break
                else:
                    ans = r.selected_option
                if r.time_taken_seconds:
                    answered_times.append((q_num, r.time_taken_seconds))

        short_q = q.question_text[:55] + '…' if len(q.question_text) > 55 else q.question_text
        row_lines.append(f"Q{q_num:<4} | {short_q:<57} | {ans:<30} | {t:<6} | {status}")

    avg = round(sum(x[1] for x in answered_times) / len(answered_times), 1) if answered_times else 0
    fastest = min(answered_times, key=lambda x: x[1]) if answered_times else None
    slowest = max(answered_times, key=lambda x: x[1]) if answered_times else None
    total_secs = latest.total_time_seconds or 0

    lines.append(f"Total Questions : {len(questions)}")
    lines.append(f"Attempted       : {attempted}")
    lines.append(f"Time Expired    : {expired}")
    lines.append(f"Not Attempted   : {len(questions) - attempted - expired}")
    lines.append(f"Average Time    : {avg} seconds/question")
    if fastest:
        lines.append(f"Fastest Answer  : Q{fastest[0]} in {fastest[1]}s")
    if slowest:
        lines.append(f"Slowest Answer  : Q{slowest[0]} in {slowest[1]}s")
    lines.append(f"Total Time      : {total_secs // 60:02d}:{total_secs % 60:02d}")
    lines.append("=" * 60)
    lines.append(f"{'Q#':<5} | {'Question':<57} | {'Your Answer':<30} | {'Time':<6} | Status")
    lines.append("-" * 60)
    lines.extend(row_lines)
    lines.append("=" * 60)
    lines.append("        — Universal AI University — The future is here —")
    lines.append("=" * 60)

    content = "\n".join(lines)
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename="UAI_Quiz_Results_{current_user.uai_id}.txt"'
    return response


@student.route('/dashboard')
@login_required
@role_required('student')
def dashboard():
    profile = current_user.student_profile
    if not profile or not profile.consent_given:
        return redirect(url_for('student.consent'))
    if not profile.age or not profile.department:
        return redirect(url_for('student.details'))

    latest_session = AssessmentSession.query.filter_by(student_id=profile.id).order_by(AssessmentSession.started_at.desc()).first()
    return render_template('student/dashboard.html', title='Student Dashboard', profile=profile, latest_session=latest_session)

@student.route('/assessment', methods=['GET'])
@login_required
@role_required('student')
def assessment_page():
    profile = current_user.student_profile
    if not profile or not profile.consent_given:
        return redirect(url_for('student.consent'))
    if not profile.age or not profile.department:
        return redirect(url_for('student.details'))
        
    # Redirect to dashboard if already completed
    latest = AssessmentSession.query.filter_by(student_id=profile.id, status='completed').first()
    if latest:
        return redirect(url_for('student.dashboard'))
        
    return render_template('student/assessment.html', title="Psychological Assessment")

@student.route('/api/assessment/session/start', methods=['POST'])
@login_required
@role_required('student')
def api_session_start():
    profile = current_user.student_profile
    if not profile:
        return jsonify({"error": "Student profile not found"}), 400
        
    session_id = session.get('assessment_session_id')
    sess_obj = None
    if session_id:
        sess_obj = AssessmentSession.query.filter_by(id=session_id, student_id=profile.id, status='in_progress').first()
        
    if not sess_obj:
        sess_obj = AssessmentSession.query.filter_by(student_id=profile.id, status='in_progress').order_by(AssessmentSession.started_at.desc()).first()
        
    resumed = False
    if sess_obj:
        resumed = True
    else:
        sess_obj = AssessmentSession(
            student_id=profile.id,
            started_at=datetime.utcnow(),
            status='in_progress'
        )
        db.session.add(sess_obj)
        db.session.commit()
        
    session['assessment_session_id'] = sess_obj.id
    
    responses = Response.query.filter_by(session_id=sess_obj.id).all()
    already_answered_ids = [r.question_id for r in responses if r.selected_option is not None or r.auto_submitted]
    
    return jsonify({
        "session_id": sess_obj.id,
        "resumed": resumed,
        "already_answered_ids": already_answered_ids
    })

@student.route('/api/assessment/questions', methods=['GET'])
@login_required
@role_required('student')
def api_questions():
    from utils.scoring import DB_NAME_MAP
    type_param = request.args.get('type', 'DASS21')
    db_name = DB_NAME_MAP.get(type_param, type_param)
    
    assessment = Assessment.query.filter_by(name=db_name).first()
    if not assessment:
        assessment = Assessment.query.filter(Assessment.name.ilike(f"%{type_param}%")).first()
        if not assessment:
            return jsonify({"error": f"Assessment {type_param} not found"}), 404
            
    questions = Question.query.filter_by(assessment_id=assessment.id).order_by(Question.order_number).all()
    
    res = []
    for q in questions:
        res.append({
            "id": q.id,
            "question_text": q.question_text,
            "category": q.category,
            "options": q.options or [],
            "order_number": q.order_number
        })
    return jsonify(res)

@student.route('/api/assessment/response', methods=['POST'])
@login_required
@role_required('student')
def api_response():
    data = request.get_json() or {}
    session_id = data.get('session_id')
    question_id = data.get('question_id')
    selected_option_index = data.get('selected_option')
    auto_skipped = data.get('auto_skipped', False)
    time_taken = data.get('time_taken_sec', 0)
    
    if not session_id or not question_id:
        return jsonify({"error": "Missing session_id or question_id"}), 400
        
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
        
    selected_value = None
    if selected_option_index is not None and not auto_skipped:
        try:
            idx = int(selected_option_index)
            if 0 <= idx < len(question.options):
                selected_value = str(question.options[idx].get('value'))
        except (ValueError, TypeError):
            pass
            
    resp = Response.query.filter_by(session_id=session_id, question_id=question_id).first()
    if resp:
        resp.selected_option = selected_value
        resp.time_taken_seconds = time_taken
        resp.auto_submitted = auto_skipped
    else:
        resp = Response(
            session_id=session_id,
            question_id=question_id,
            selected_option=selected_value,
            time_taken_seconds=time_taken,
            auto_submitted=auto_skipped
        )
        db.session.add(resp)
        
    db.session.commit()
    return jsonify({"success": True})

@student.route('/api/assessment/session/submit', methods=['POST'])
@login_required
@role_required('student')
def api_session_submit():
    from utils.scoring import calculate_scores, determine_overall_risk
    data = request.get_json() or {}
    session_id = data.get('session_id')
    total_time = data.get('total_time_seconds', 0)
    
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400
        
    sess_obj = AssessmentSession.query.get(session_id)
    if not sess_obj:
        return jsonify({"error": "Session not found"}), 404
        
    sess_obj.completed_at = datetime.utcnow()
    sess_obj.status = 'completed'
    sess_obj.total_time_seconds = total_time
    
    try:
        dass_score = calculate_scores(sess_obj, "DASS21")
        bfi_score = calculate_scores(sess_obj, "BFI44")
        eq_score = calculate_scores(sess_obj, "EQ")
        sq_score = calculate_scores(sess_obj, "SQ")
        home_score = calculate_scores(sess_obj, "HOME")
        
        all_scores = {
            "DASS21": dass_score,
            "BFI44": bfi_score,
            "EQ": eq_score,
            "SQ": sq_score,
            "HOME": home_score
        }
        
        risk_data = determine_overall_risk(all_scores)
        risk_level = risk_data["risk_level"]
        
        from app.models import AssessmentScore
        assessments = Assessment.query.all()
        for ass in assessments:
            score_data = None
            total_score = 0.0
            severity = ""
            
            if ass.name == "DASS-21":
                score_data = dass_score
                total_score = float(dass_score["total_score"])
                severity = risk_level.capitalize()
            elif ass.name == "BFI-44":
                score_data = bfi_score
                total_score = float(bfi_score["total_score"])
                severity = bfi_score["severity_labels"].get("Neuroticism", "")
            elif ass.name == "EQ":
                score_data = eq_score
                total_score = float(eq_score["total_score"])
                severity = eq_score["severity_labels"]["Emotional Awareness"]
            elif ass.name == "SQ":
                score_data = sq_score
                total_score = float(sq_score["total_score"])
                severity = sq_score["severity_labels"]["Social Awareness"]
            elif ass.name == "Home Adjustment Questionnaire":
                score_data = home_score
                total_score = float(home_score["total_score"])
                severity = home_score["severity_labels"]["Home Adjustment"]
                
            if score_data:
                AssessmentScore.query.filter_by(session_id=sess_obj.id, assessment_id=ass.id).delete()
                
                score_rec = AssessmentScore(
                    session_id=sess_obj.id,
                    assessment_id=ass.id,
                    category_scores=score_data,
                    total_score=total_score,
                    severity_label=severity
                )
                db.session.add(score_rec)
                
        profile = StudentProfile.query.get(sess_obj.student_id)
        if profile:
            profile.risk_level = risk_level.capitalize()
            
            if risk_level in ["high", "severe"]:
                from app.models import Flag
                flag = Flag(
                    student_id=profile.user_id,
                    counsellor_id=profile.assigned_counsellor_id,
                    reason=f"Automated risk flag: {risk_level.upper()} severity detected in DASS-21 assessment session {sess_obj.id}.",
                    created_at=datetime.utcnow()
                )
                db.session.add(flag)
                
        db.session.commit()
        session.pop('assessment_session_id', None)
        return jsonify({"success": True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Scoring calculation failed: {str(e)}"}), 500
