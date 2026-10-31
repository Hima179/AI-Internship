import os
import sys

# Ensure the root directory is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Question, Response, Assessment

DB_NAME_MAP = {
    "DASS21": "DASS-21",
    "BFI44": "BFI-44",
    "EQ": "EQ",
    "SQ": "SQ",
    "HOME": "Home Adjustment Questionnaire"
}

def calculate_scores(session, assessment_name):
    """
    Calls the correct scorer based on assessment_name.
    
    Parameters:
    session (AssessmentSession): The assessment session object.
    assessment_name (str): The assessment name (DASS21, BFI44, EQ, SQ, HOME).
    
    Returns:
    dict: The scoring results from the delegated scorer.
    """
    db_name = DB_NAME_MAP.get(assessment_name, assessment_name)
    assessment = Assessment.query.filter_by(name=db_name).first()
    
    if not assessment:
        # Fallback case-insensitive check
        assessment = Assessment.query.filter(Assessment.name.ilike(f"%{assessment_name}%")).first()
        if not assessment:
            raise ValueError(f"Assessment '{assessment_name}' (mapped to '{db_name}') not found in database.")
    
    # Fetch questions and responses
    questions = Question.query.filter_by(assessment_id=assessment.id).order_by(Question.order_number).all()
    responses = Response.query.filter_by(session_id=session.id).join(Question).filter(Question.assessment_id == assessment.id).all()
    
    name_upper = assessment_name.upper()
    if name_upper in ["DASS21", "DASS-21"]:
        return _score_dass21(questions, responses)
    elif name_upper in ["BFI44", "BFI-44"]:
        return _score_bfi44(questions, responses)
    elif name_upper == "EQ":
        return _score_eq_sq(questions, responses, "EQ")
    elif name_upper == "SQ":
        return _score_eq_sq(questions, responses, "SQ")
    elif name_upper in ["HOME", "HOME ADJUSTMENT", "HOME_ADJUSTMENT"] or "Home" in assessment.name:
        return _score_home_adjustment(questions, responses)
    else:
        raise ValueError(f"Unsupported assessment name for scoring: {assessment_name}")

def _score_dass21(questions, responses):
    """
    Scores DASS-21 responses.
    - Group questions by category (Depression/Anxiety/Stress)
    - Sum selected_option values per category (0-3 scale)
    - MULTIPLY EACH SUM BY 2
    - Apply severity classification
    """
    # Map question ID to selected option (default 0 if missing)
    resp_map = {}
    for r in responses:
        try:
            resp_map[r.question_id] = int(r.selected_option or 0)
        except ValueError:
            resp_map[r.question_id] = 0

    category_sums = {"Depression": 0, "Anxiety": 0, "Stress": 0}
    for q in questions:
        cat = q.category # e.g. "Depression", "Anxiety", "Stress"
        if cat in category_sums:
            category_sums[cat] += resp_map.get(q.id, 0)
            
    # Multiply each sum by 2
    category_scores = {cat: sum_val * 2 for cat, sum_val in category_sums.items()}
    total_score = sum(category_scores.values())
    
    severity_labels = {}
    interpretations = {}
    
    # 1. Depression Scoring
    dep_score = category_scores["Depression"]
    if dep_score <= 9:
        severity_labels["Depression"] = "Normal"
        interpretations["Depression"] = "Normal. No significant depressive symptoms detected."
    elif dep_score <= 13:
        severity_labels["Depression"] = "Mild"
        interpretations["Depression"] = "Mild depressive symptoms. Periodic low mood or mild discouragement."
    elif dep_score <= 20:
        severity_labels["Depression"] = "Moderate"
        interpretations["Depression"] = "Noticeable feelings of sadness, hopelessness, and lack of interest or initiative."
    elif dep_score <= 27:
        severity_labels["Depression"] = "Severe"
        interpretations["Depression"] = "Severe depressive symptoms. Substantial feelings of sadness, worthlessness, and loss of energy."
    else:
        severity_labels["Depression"] = "Extremely Severe"
        interpretations["Depression"] = "Extremely severe depressive symptoms. Pervasive low mood and loss of pleasure. Professional clinical evaluation is recommended."

    # 2. Anxiety Scoring
    anx_score = category_scores["Anxiety"]
    if anx_score <= 7:
        severity_labels["Anxiety"] = "Normal"
        interpretations["Anxiety"] = "Normal. No significant anxiety symptoms detected."
    elif anx_score <= 9:
        severity_labels["Anxiety"] = "Mild"
        interpretations["Anxiety"] = "Mild anxiety. Occasional worry or mild physical tension."
    elif anx_score <= 14:
        severity_labels["Anxiety"] = "Moderate"
        interpretations["Anxiety"] = "Moderate anxiety. Noticeable worry, muscle tension, or situational apprehension."
    elif anx_score <= 19:
        severity_labels["Anxiety"] = "Severe"
        interpretations["Anxiety"] = "Persistent fear, panic, and physical symptoms of anxiety (e.g. rapid breathing, trembling)."
    else:
        severity_labels["Anxiety"] = "Extremely Severe"
        interpretations["Anxiety"] = "Extremely severe anxiety and panic symptoms. Persistent physical distress and apprehension. Professional evaluation is recommended."

    # 3. Stress Scoring
    str_score = category_scores["Stress"]
    if str_score <= 14:
        severity_labels["Stress"] = "Normal"
        interpretations["Stress"] = "Normal. No significant stress-related symptoms detected."
    elif str_score <= 18:
        severity_labels["Stress"] = "Mild"
        interpretations["Stress"] = "Mild stress. Slightly elevated tension, difficulty winding down at times."
    elif str_score <= 25:
        severity_labels["Stress"] = "Moderate"
        interpretations["Stress"] = "Moderate stress. Finding it hard to relax, irritation, or feeling overcommitted."
    elif str_score <= 33:
        severity_labels["Stress"] = "Severe"
        interpretations["Stress"] = "Significant stress-related symptoms. High nervous energy, touchiness, and agitation."
    else:
        severity_labels["Stress"] = "Extremely Severe"
        interpretations["Stress"] = "Extremely severe stress. Difficulty coping with demands, persistent inability to relax. Professional guidance is recommended."
        
    return {
        "category_scores": category_scores,
        "severity_labels": severity_labels,
        "total_score": total_score,
        "interpretations": interpretations
    }

def _score_bfi44(questions, responses):
    """
    Scores BFI-44 responses.
    - For reverse_scored items: reverse_score = 6 - original_score
    - Group by dimension (Extraversion/Agreeableness/Conscientiousness/Neuroticism/Openness)
    - Calculate MEAN for each dimension
    - Apply interpretation (1.0-2.4=Low, 2.5-3.4=Moderate, 3.5-5.0=High)
    - Generate counselling flags
    """
    resp_map = {r.question_id: r for r in responses}
    
    dimensions = ["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"]
    dim_scores = {d: [] for d in dimensions}
    
    for q in questions:
        dim = q.category # e.g. "Extraversion", "Agreeableness", etc.
        if dim not in dim_scores:
            continue
            
        r = resp_map.get(q.id)
        if not r or r.selected_option is None:
            val = 3  # Default to Neutral if unanswered
        else:
            try:
                val = int(r.selected_option)
            except ValueError:
                val = 3
                
        # Check if question is reverse scored
        is_reverse = getattr(q, 'reverse_scored', False)
        if is_reverse:
            val = 6 - val
            
        dim_scores[dim].append(val)
        
    category_scores = {}
    severity_labels = {}
    all_means = []
    
    for dim in dimensions:
        scores = dim_scores[dim]
        if scores:
            mean_val = sum(scores) / len(scores)
        else:
            mean_val = 3.0
            
        mean_val = round(mean_val, 2)
        category_scores[dim] = mean_val
        all_means.append(mean_val)
        
        # Apply dimension range labels
        if mean_val < 2.5:
            severity_labels[dim] = "Low"
        elif mean_val <= 3.4:
            severity_labels[dim] = "Moderate"
        else:
            severity_labels[dim] = "High"
            
    # Calculate overall mean
    total_score = round(sum(all_means) / len(all_means), 2) if all_means else 3.0
    
    # Check counselling flags
    counselling_flags = []
    if category_scores.get("Neuroticism", 0.0) >= 3.5:
        counselling_flags.append("Emotionally reactive, anxiety risk")
    if category_scores.get("Conscientiousness", 0.0) <= 2.4:
        counselling_flags.append("Academic performance risk")
    if category_scores.get("Agreeableness", 0.0) <= 2.4:
        counselling_flags.append("Interpersonal conflict risk")
        
    return {
        "category_scores": category_scores,
        "severity_labels": severity_labels,
        "counselling_flags": counselling_flags,
        "total_score": total_score
    }

def _score_eq_sq(questions, responses, assessment_name):
    """
    Scores EQ or SQ responses.
    - Sum all 8 responses (1-5 scale)
    - Scoring ranges: 8-18 = Low, 19-30 = Moderate, 31-40 = High
    """
    resp_map = {r.question_id: r for r in responses}
    total_score = 0
    
    for q in questions:
        r = resp_map.get(q.id)
        if not r or r.selected_option is None:
            val = 3  # Default to Neutral
        else:
            try:
                val = int(r.selected_option)
            except ValueError:
                val = 3
        total_score += val
        
    if total_score <= 18:
        severity = "Low"
    elif total_score <= 30:
        severity = "Moderate"
    else:
        severity = "High"
        
    category = "Emotional Awareness" if assessment_name.upper() == "EQ" else "Social Awareness"
    
    return {
        "category_scores": {category: total_score},
        "severity_labels": {category: severity},
        "total_score": total_score
    }

def _score_home_adjustment(questions, responses):
    """
    Scores Home Adjustment responses.
    - Sum all 15 items (0-1 scale)
    - Ranges: 0-4 = Healthy, 5-9 = Mild Concerns, 10-15 = Significant Difficulties
    """
    resp_map = {r.question_id: r for r in responses}
    total_score = 0
    
    for q in questions:
        r = resp_map.get(q.id)
        if not r or r.selected_option is None:
            val = 0  # Default to Not True (0)
        else:
            try:
                val = int(r.selected_option)
            except ValueError:
                val = 0
        total_score += val
        
    if total_score <= 4:
        severity = "Healthy"
    elif total_score <= 9:
        severity = "Mild Concerns"
    else:
        severity = "Significant Difficulties"
        
    return {
        "category_scores": {"Home Adjustment": total_score},
        "severity_labels": {"Home Adjustment": severity},
        "total_score": total_score
    }

def determine_overall_risk(all_scores_dict):
    """
    Takes a dict of all assessment scores for one student and determines
    overall risk level and counselling recommendations.
    
    Parameters:
    all_scores_dict (dict): A dictionary where keys are assessment names
                            (DASS21, BFI44, EQ, SQ, HOME) and values are
                            their respective scoring output dictionaries.
                            
    Returns:
    dict: A dictionary containing 'risk_level', 'counselling_recommendations',
          and 'eq_sq_interpretation'.
    """
    # 1. Extract values or use defaults
    dep_score = 0
    anx_score = 0
    str_score = 0
    home_score = 0
    neuro_score = 0.0
    eq_score = 30
    sq_score = 30
    
    dass_data = all_scores_dict.get("DASS21") or all_scores_dict.get("DASS-21") or {}
    if dass_data:
        cat_scores = dass_data.get("category_scores", {})
        dep_score = cat_scores.get("Depression", 0)
        anx_score = cat_scores.get("Anxiety", 0)
        str_score = cat_scores.get("Stress", 0)
        
    home_data = all_scores_dict.get("HOME") or all_scores_dict.get("Home Adjustment Questionnaire") or {}
    if home_data:
        home_score = home_data.get("total_score", 0)
        
    bfi_data = all_scores_dict.get("BFI44") or all_scores_dict.get("BFI-44") or {}
    if bfi_data:
        neuro_score = bfi_data.get("category_scores", {}).get("Neuroticism", 0.0)
        
    eq_data = all_scores_dict.get("EQ") or {}
    if eq_data:
        eq_score = eq_data.get("total_score", 30)
        
    sq_data = all_scores_dict.get("SQ") or {}
    if sq_data:
        sq_score = sq_data.get("total_score", 30)

    # 2. Combined EQ+SQ profile interpretation
    eq_low = (eq_score <= 18)
    sq_low = (sq_score <= 18)
    
    if not eq_low and not sq_low:
        eq_sq_interpretation = "Strong emotional and social functioning"
    elif not eq_low and sq_low:
        eq_sq_interpretation = "Good emotional awareness but social difficulty"
    elif eq_low and not sq_low:
        eq_sq_interpretation = "Social capable but emotional regulation issues"
    else:  # eq_low and sq_low
        eq_sq_interpretation = "Challenges in both domains, support needed"

    # 3. Determine Risk Level (in priority order)
    # SEVERE: DASS Depression>=28 OR Anxiety>=20 OR Stress>=34
    if dep_score >= 28 or anx_score >= 20 or str_score >= 34:
        risk_level = "severe"
        recommendations = [
            "Urgent: Immediate clinical intervention is recommended.",
            "Schedule a priority one-on-one session with the head counsellor.",
            "Notify emergency contact or student welfare department if necessary.",
            "Provide contact info for 24/7 mental health helpline."
        ]
    # HIGH: DASS Depression>=21 OR Anxiety>=15 OR Stress>=26 OR Home Adjustment >= 10
    elif dep_score >= 21 or anx_score >= 15 or str_score >= 26 or home_score >= 10:
        risk_level = "high"
        recommendations = [
            "High Priority: Schedule a counselling session within 24-48 hours.",
            "Conduct a follow-up assessment to monitor symptoms.",
            "Recommend stress management and coping strategy workshops.",
            "Recommend close academic mentoring due to potential impact."
        ]
    # MEDIUM: DASS Depression>=14 OR Anxiety>=10 OR Stress>=19 OR BFI Neuroticism >= 3.5 OR EQ score <= 18 OR SQ score <= 18 OR Home Adjustment >= 5
    elif (dep_score >= 14 or anx_score >= 10 or str_score >= 19 or 
          neuro_score >= 3.5 or 
          eq_low or sq_low or 
          home_score >= 5):
        risk_level = "medium"
        recommendations = [
            "Routine follow-up: Suggest scheduling a counselling session within a week.",
            "Encourage participation in emotional intelligence (EQ) or social skills (SQ) group activities.",
            "Recommend online self-help resources and mindfulness training.",
            "Suggest regular check-ins with faculty advisors."
        ]
    # LOW: All others
    else:
        risk_level = "low"
        recommendations = [
            "No immediate action needed. Encourage maintaining current healthy habits.",
            "Provide general wellness resources.",
            "Suggest periodic self-reassessment."
        ]
        
    # Append specific recommendations based on scoring details
    if eq_low:
        recommendations.append("Recommend workshops focusing on emotional regulation and empathy development.")
    if sq_low:
        recommendations.append("Recommend social skills training or joining group activities to build social confidence.")
    if home_score >= 10:
        recommendations.append("Highly recommend family counselling or conflict resolution support.")
    elif home_score >= 5:
        recommendations.append("Suggest family relationship support resources.")
    if neuro_score >= 3.5:
        recommendations.append("Suggest cognitive behavioral techniques (CBT) for managing emotional reactivity.")
        
    return {
        "risk_level": risk_level,
        "counselling_recommendations": recommendations,
        "eq_sq_interpretation": eq_sq_interpretation
    }
