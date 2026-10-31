from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'username'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='student') # student, counsellor, faculty
    
    registration = db.relationship('Registration', backref='user', uselist=False)
    details = db.relationship('Detail', backref='user', uselist=False)

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        # We will support both plain text (for existing users) and hashed
        if self.password.startswith('scrypt:'):
            return check_password_hash(self.password, pwd)
        return self.password == pwd

    def __repr__(self):
        return f'<User {self.username}>'

class Registration(db.Model):
    __tablename__ = 'registration'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('username.id'), nullable=False)
    registration_number = db.Column(db.String(50), unique=True, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Registration {self.registration_number}>'

class Detail(db.Model):
    __tablename__ = 'details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('username.id'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)

    def __repr__(self):
        return f'<Detail {self.full_name}>'
