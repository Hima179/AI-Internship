import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from ..models import User

class RegisterForm(FlaskForm):
    uai_id = StringField('UAI ID', validators=[DataRequired(), Length(min=4, max=64)])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    role = RadioField('Role', choices=[('student', 'Student'), ('counsellor', 'Counsellor'), ('faculty', 'Faculty')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_uai_id(self, uai_id):
        user = User.query.filter_by(uai_id=uai_id.data).first()
        if user:
            raise ValidationError('This UAI ID is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')

    def validate_password(self, password):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(pattern, password.data):
            raise ValidationError('Password must be at least 8 characters long and contain uppercase, lowercase, numbers, and special characters.')

class LoginForm(FlaskForm):
    uai_id = StringField('UAI ID or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
