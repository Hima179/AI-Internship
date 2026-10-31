from .models import db, AssessmentSession, Question, Response, AssessmentScore, StudentProfile, Flag, Assessment
from datetime import datetime

def calculate_dass21(session_id):
    responses = Response.query.join(Question).filter(
        Response.session_id == session_id,
        Question.assessment_id == Assessment.query.filter_by(name='DASS-21').first().id
    ).all()
    
    # Map responses by question order_number
    resp_map = {r.question.order_number: int(r.selected_option or 0) for r in responses}
    
    depression_indices = [3, 5, 10, 13, 16, 17, 21]
    anxiety_indices = [2, 4, 7, 9, 15, 19, 20]
    stress_indices = [1, 6, 8, 11, 12, 14, 18]
    
    d_score = sum(resp_map.get(i, 0) for i in depression_indices) * 2
    a_score = sum(resp_map.get(i, 0) for i in anxiety_indices) * 2
    s_score = sum(resp_map.get(i, 0) for i in stress_indices) * 2
    
    def get_severity(score, scale):
        if scale == 'depression':
            if score <= 9: return "Normal"
            if score <= 13: return "Mild"
            if score <= 20: return "Moderate"
            if score <= 27: return "Severe"
            return "Extremely Severe"
        if scale == 'anxiety':
            if score <= 7: return "Normal"
            if score <= 9: return "Mild"
            if score <= 14: return "Moderate"
            if score <= 19: return "Severe"
            return "Extremely Severe"
        if scale == 'stress':
            if score <= 14: return "Normal"
            if score <= 18: return "Mild"
            if score <= 25: return "Moderate"
            if score <= 33: return "Severe"
            return "Extremely Severe"
        return "Unknown"

    return {
        "depression": {"score": d_score, "severity": get_severity(d_score, 'depression')},
        "anxiety": {"score": a_score, "severity": get_severity(a_score, 'anxiety')},
        "stress": {"score": s_score, "severity": get_severity(s_score, 'stress')}
    }

def calculate_bfi44(session_id):
    responses = Response.query.join(Question).filter(
        Response.session_id == session_id,
        Question.assessment_id == Assessment.query.filter_by(name='BFI-44').first().id
    ).all()
    
    # Traits and their question indices (1-indexed based on order_number)
    # Note: Reverse items are standard for BFI-44
    traits = {
        "Extraversion": {"items": [1, 6, 11, 16, 21, 26, 31, 36], "reverse": [6, 21, 31]},
        "Agreeableness": {"items": [2, 7, 12, 17, 22, 27, 32, 37, 42], "reverse": [2, 12, 27, 37]},
        "Conscientiousness": {"items": [3, 8, 13, 18, 23, 28, 33, 38, 43], "reverse": [8, 18, 23, 43]},
        "Neuroticism": {"items": [4, 9, 14, 19, 24, 29, 34, 39], "reverse": [9, 24, 34]},
        "Openness": {"items": [5, 10, 15, 20, 25, 30, 35, 40, 41, 44], "reverse": [35, 41]}
    }
    
    resp_map = {r.question.order_number: int(r.selected_option or 3) for r in responses} # Default to neutral if missing
    
    results = {}
    for trait, info in traits.items():
        trait_scores = []
        for i in info["items"]:
            val = resp_map.get(i, 3)
            if i in info["reverse"]:
                val = 6 - val
            trait_scores.append(val)
        
        avg_score = sum(trait_scores) / len(trait_scores)
        level = "Low" if avg_score < 2.5 else ("Medium" if avg_score <= 3.5 else "High")
        results[trait.lower()] = {"score": round(avg_score, 2), "level": level}
        
    return results

def calculate_eq(session_id):
    responses = Response.query.join(Question).filter(
        Response.session_id == session_id,
        Question.assessment_id == Assessment.query.filter_by(name='EQ').first().id
    ).all()
    
    total_score = sum(int(r.selected_option or 0) for r in responses)
    # Simple mapping for classification
    category = "Low" if total_score < 30 else ("Average" if total_score <= 52 else ("Above Average" if total_score <= 63 else "High"))
    return {"total_score": total_score, "category": category}

def calculate_sq(session_id):
    responses = Response.query.join(Question).filter(
        Response.session_id == session_id,
        Question.assessment_id == Assessment.query.filter_by(name='SQ').first().id
    ).all()
    
    total_score = sum(int(r.selected_option or 0) for r in responses)
    category = "Low" if total_score < 30 else ("Average" if total_score <= 52 else ("Above Average" if total_score <= 63 else "High"))
    return {"total_score": total_score, "category": category}

def determine_risk_level(dass_scores):
    severities = [dass_scores['depression']['severity'], dass_scores['anxiety']['severity'], dass_scores['stress']['severity']]
    if any(s in ["Severe", "Extremely Severe"] for s in severities):
        return "Severe"
    if any(s == "Moderate" for s in severities):
        return "Moderate"
    if any(s == "Mild" for s in severities):
        return "Mild"
    return "Normal"

def run_all_scores(session_id):
    session = AssessmentSession.query.get(session_id)
    if not session: return None
    
    dass_results = calculate_dass21(session_id)
    bfi_results = calculate_bfi44(session_id)
    eq_results = calculate_eq(session_id)
    sq_results = calculate_sq(session_id)
    
    risk_level = determine_risk_level(dass_results)
    
    # Save results to AssessmentScore
    assessments = Assessment.query.all()
    for ass in assessments:
        score_data = None
        total_score = 0
        severity = ""
        
        if ass.name == 'DASS-21':
            score_data = dass_results
            total_score = dass_results['depression']['score'] + dass_results['anxiety']['score'] + dass_results['stress']['score']
            severity = risk_level
        elif ass.name == 'BFI-44':
            score_data = bfi_results
            total_score = sum(v['score'] for v in bfi_results.values()) / 5
        elif ass.name == 'EQ':
            score_data = eq_results
            total_score = eq_results['total_score']
            severity = eq_results['category']
        elif ass.name == 'SQ':
            score_data = sq_results
            total_score = sq_results['total_score']
            severity = sq_results['category']
            
        if score_data:
            score_rec = AssessmentScore(
                session_id=session_id,
                assessment_id=ass.id,
                category_scores=score_data,
                total_score=total_score,
                severity_label=severity
            )
            db.session.add(score_rec)
    
    # Update Student Profile
    profile = StudentProfile.query.get(session.student_id)
    if profile:
        profile.risk_level = risk_level
        
        # Auto-create Flag if high risk
        if risk_level in ["Moderate", "Severe"]:
            flag = Flag(
                student_id=profile.user_id,
                reason=f"Automated risk flag: {risk_level} severity detected in DASS-21.",
                created_at=datetime.utcnow()
            )
            db.session.add(flag)
            
    db.session.commit()
    
    return {
        "dass21": dass_results,
        "bfi44": bfi_results,
        "eq": eq_results,
        "sq": sq_results,
        "risk_level": risk_level
    }
