from flask import render_template
from flask_login import login_required, current_user
from . import faculty
from ..auth import role_required
from ..models import db, StudentProfile, AssessmentSession, Flag
from sqlalchemy import func

@faculty.route('/dashboard')
@login_required
@role_required('faculty')
def dashboard():
    # KPI: Total Assessments
    total_assessments = AssessmentSession.query.filter_by(status='completed').count()
    
    # KPI: Total Active Flags (Anonymized)
    active_flags = Flag.query.filter_by(is_resolved=False).count()
    
    # Risk Distribution (Overall)
    risk_counts = db.session.query(
        StudentProfile.risk_level, func.count(StudentProfile.id)
    ).filter(StudentProfile.risk_level.isnot(None)).group_by(StudentProfile.risk_level).all()
    
    risk_data = {
        'Normal': 0, 'Mild': 0, 'Moderate': 0, 'Severe': 0
    }
    for r_level, count in risk_counts:
        if r_level in risk_data:
            risk_data[r_level] = count
            
    # Department Breakdown
    dept_risk_counts = db.session.query(
        StudentProfile.department, StudentProfile.risk_level, func.count(StudentProfile.id)
    ).filter(StudentProfile.risk_level.isnot(None)).group_by(StudentProfile.department, StudentProfile.risk_level).all()
    
    dept_data = {}
    for dept, r_level, count in dept_risk_counts:
        if dept not in dept_data:
            dept_data[dept] = {'Normal': 0, 'Mild': 0, 'Moderate': 0, 'Severe': 0}
        if r_level in dept_data[dept]:
            dept_data[dept][r_level] = count
            
    # Prepare labels and dataset arrays for Chart.js
    dept_labels = list(dept_data.keys())
    dept_moderate_severe = []
    for dept in dept_labels:
        total_risk = dept_data[dept]['Moderate'] + dept_data[dept]['Severe']
        dept_moderate_severe.append(total_risk)
        
    chart_data = {
        "overall_risk": {
            "labels": list(risk_data.keys()),
            "data": list(risk_data.values())
        },
        "dept_risk": {
            "labels": dept_labels,
            "data": dept_moderate_severe
        }
    }
    
    return render_template('faculty/dashboard.html', 
                           kpis={'total_assessments': total_assessments, 'active_flags': active_flags},
                           chart_data=chart_data,
                           dept_data=dept_data)
