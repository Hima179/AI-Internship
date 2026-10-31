from app import create_app, db
from app.models import User, StudentProfile, AssessmentSession, AssessmentScore, Flag, Assessment

app = create_app('development')
with app.app_context():
    # Use the first counsellor for testing
    counsellor = User.query.filter_by(role='counsellor').first()
    
    # Base queries for students assigned to this counsellor
    assigned_students = StudentProfile.query.filter_by(assigned_counsellor_id=counsellor.id).all()
    student_ids = [s.id for s in assigned_students]
    user_ids = [s.user_id for s in assigned_students]

    # KPIs
    total_assessed = AssessmentSession.query.filter(AssessmentSession.student_id.in_(student_ids), AssessmentSession.status == 'completed').count()
    flagged = Flag.query.filter_by(counsellor_id=counsellor.id, is_resolved=False).count()
    
    moderate_stress = StudentProfile.query.filter(StudentProfile.id.in_(student_ids), StudentProfile.risk_level == 'Moderate').count()
    
    # We need to query AssessmentScore for BFI-44 where category_scores->'neuroticism'->>'level' == 'High'
    # SQLite JSON querying is a bit tricky, so let's do it in python memory for now since dataset is small
    high_neuroticism = 0
    low_eq_risk = 0
    
    scores = AssessmentScore.query.join(AssessmentSession).filter(AssessmentSession.student_id.in_(student_ids)).all()
    for score in scores:
        if score.assessment.name == 'BFI-44':
            if score.category_scores and score.category_scores.get('neuroticism', {}).get('level') == 'High':
                high_neuroticism += 1
        elif score.assessment.name == 'EQ':
            if score.severity_label == 'Low':
                low_eq_risk += 1

    print(f"Total Assessed: {total_assessed}")
    print(f"Flagged: {flagged}")
    print(f"Moderate Stress: {moderate_stress}")
    print(f"High Neuroticism: {high_neuroticism}")
    print(f"Low EQ Risk: {low_eq_risk}")
