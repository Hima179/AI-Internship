from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager, bcrypt

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uai_id = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20)) # student/counsellor/faculty
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, index=True)
    department = db.Column(db.String(100), nullable=True)  # faculty/counsellor department
    designation = db.Column(db.String(100), nullable=True)  # e.g. Professor, HOD, Dean
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    student_profile = db.relationship('StudentProfile', foreign_keys='StudentProfile.user_id', backref='user', uselist=False)
    flags_raised = db.relationship('Flag', foreign_keys='Flag.counsellor_id', backref='counsellor')
    student_flags = db.relationship('Flag', foreign_keys='Flag.student_id', backref='student')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.uai_id}>'

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    course = db.Column(db.String(100))
    year_of_study = db.Column(db.Integer)
    department = db.Column(db.String(100))
    consent_given = db.Column(db.Boolean, default=False)
    consent_timestamp = db.Column(db.DateTime)
    assigned_counsellor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    risk_level = db.Column(db.String(20), default=None) # Normal/Mild/Moderate/Severe
    phone = db.Column(db.String(15))
    previous_counselling = db.Column(db.String(10)) # yes/no
    mental_health_diagnosis = db.Column(db.String(20)) # yes/no/prefer_not_to_say

    assigned_counsellor = db.relationship('User', foreign_keys=[assigned_counsellor_id], backref='assigned_students')

    # Sessions
    sessions = db.relationship('AssessmentSession', backref='student_profile')

    def __repr__(self):
        return f'<StudentProfile {self.user_id}>'

class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100)) # DASS-21/BFI-44/EQ/SQ
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    questions = db.relationship('Question', backref='assessment')
    scores = db.relationship('AssessmentScore', backref='assessment')

    def __repr__(self):
        return f'<Assessment {self.name}>'

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    question_text = db.Column(db.Text)
    category = db.Column(db.String(100))
    options = db.Column(db.JSON) # list of dicts with value and label
    order_number = db.Column(db.Integer)
    time_limit = db.Column(db.Integer, default=10)
    reverse_scored = db.Column(db.Boolean, default=False)

    responses = db.relationship('Response', backref='question')

    def __repr__(self):
        return f'<Question {self.id} of {self.assessment_id}>'

class AssessmentSession(db.Model):
    __tablename__ = 'assessment_sessions'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'))
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    total_time_seconds = db.Column(db.Integer)
    status = db.Column(db.String(20), default='in_progress') # in_progress/completed/abandoned

    responses = db.relationship('Response', backref='session')
    scores = db.relationship('AssessmentScore', backref='session')

    def __repr__(self):
        return f'<AssessmentSession {self.id}>'

class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('assessment_sessions.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    selected_option = db.Column(db.String(255), nullable=True)
    time_taken_seconds = db.Column(db.Integer)
    auto_submitted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Response session:{self.session_id} question:{self.question_id}>'

class AssessmentScore(db.Model):
    __tablename__ = 'assessment_scores'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('assessment_sessions.id'))
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    category_scores = db.Column(db.JSON)
    total_score = db.Column(db.Float)
    severity_label = db.Column(db.String(50))

    def __repr__(self):
        return f'<AssessmentScore session:{self.session_id}>'

class Flag(db.Model):
    __tablename__ = 'flags'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    counsellor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_resolved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Flag student:{self.student_id} reason:{self.reason[:20]}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
