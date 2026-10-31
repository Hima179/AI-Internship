from models.user import db
from datetime import datetime

class Consent(db.Model):
    __tablename__ = 'consents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('username.id'), nullable=False)
    agreed = db.Column(db.Boolean, nullable=False, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='consent', uselist=False)

    def __repr__(self):
        return f'<Consent User:{self.user_id} Agreed:{self.agreed}>'

class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('username.id'), nullable=False)
    
    # DASS-21 Subscale Scores
    depression_score = db.Column(db.Integer, nullable=False)
    anxiety_score = db.Column(db.Integer, nullable=False)
    stress_score = db.Column(db.Integer, nullable=False)
    
    # Optional raw JSON of all answers if needed for future analytics
    raw_data = db.Column(db.Text, nullable=True) 
    
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='survey_responses')

    def __repr__(self):
        return f'<SurveyResponse User:{self.user_id}>'
