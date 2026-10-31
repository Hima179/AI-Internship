from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.user import db
from models.survey import Consent, SurveyResponse

survey_bp = Blueprint('survey', __name__)

@survey_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@survey_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    if request.method == 'POST':
        # Ensure user consented
        consent = Consent.query.filter_by(user_id=current_user.id).first()
        if not consent or not consent.agreed:
            flash("You must agree to the consent form before taking the survey.", "error")
            return redirect(url_for('survey.consent'))

        # Calculate scores
        depression = 0
        anxiety = 0
        stress = 0
        
        # DASS-21 scoring mapping based on the form structure
        for i in range(1, 8):
            depression += int(request.form.get(f'q{i}', 0))
        for i in range(8, 15):
            anxiety += int(request.form.get(f'q{i}', 0))
        for i in range(15, 22):
            stress += int(request.form.get(f'q{i}', 0))

        # Save to DB
        new_response = SurveyResponse(
            user_id=current_user.id,
            depression_score=depression * 2, # DASS-21 is typically multiplied by 2 to match DASS-42
            anxiety_score=anxiety * 2,
            stress_score=stress * 2
        )
        db.session.add(new_response)
        db.session.commit()
        
        flash("Awesome! Your survey responses have been securely saved.", "success")
        return redirect(url_for('survey.dashboard'))
        
    return render_template('survey.html')

@survey_bp.route('/consent', methods=['GET', 'POST'])
@login_required
def consent():
    if request.method == 'POST':
        # Check if already consented
        existing = Consent.query.filter_by(user_id=current_user.id).first()
        if not existing:
            new_consent = Consent(user_id=current_user.id, agreed=True)
            db.session.add(new_consent)
            db.session.commit()
        return redirect(url_for('survey.survey'))
        
    return render_template('consent.html')
