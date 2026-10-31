from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional

class StudentDetailsForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=16, max=40)])
    gender = SelectField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('non-binary', 'Non-binary'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], validators=[DataRequired()])
    department = SelectField('Department / Programme', choices=[
        ('', '— Select your Department —'),
        # BTech Programmes
        ('BTech AI & ML', 'BTech – Artificial Intelligence & Machine Learning'),
        ('BTech Data Science', 'BTech – Data Science'),
        ('BTech Computer Science', 'BTech – Computer Science & Engineering'),
        ('BTech Sound Engineering', 'BTech – Sound Engineering & Music Technology'),
        # BSc Programmes
        ('BSc Psychology', 'BSc – Psychology'),
        ('BSc Data Science', 'BSc – Data Science'),
        ('BSc AI', 'BSc – Artificial Intelligence'),
        ('BSc Computer Science', 'BSc – Computer Science'),
        # BBA / MBA
        ('BBA General', 'BBA – General Management'),
        ('BBA Marketing', 'BBA – Marketing & Branding'),
        ('BBA Finance', 'BBA – Finance & Accounting'),
        ('MBA General', 'MBA – General Management'),
        ('MBA AI & Business', 'MBA – AI & Business Analytics'),
        ('MBA Marketing', 'MBA – Marketing'),
        ('MBA Finance', 'MBA – Finance'),
        # Design
        ('BDes', 'BDes – Bachelor of Design'),
        ('MDes', 'MDes – Master of Design'),
        # Media & Arts
        ('BA Liberal Arts', 'BA – Liberal Arts & Social Sciences'),
        ('BA Music', 'BA – Music & Cinematics'),
        ('BA Film', 'BA – Film & Media Production'),
        # Other
        ('Other', 'Other / Not Listed'),
    ], validators=[DataRequired()])
    year_of_study = SelectField('Year of Study', choices=[
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year')
    ], coerce=int, validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=15)])
    previous_counselling = RadioField('Have you ever attended counselling before?', choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ], validators=[DataRequired()])
    mental_health_diagnosis = RadioField('Do you have any previously diagnosed mental health conditions?', choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], validators=[DataRequired()])
    submit = SubmitField('Save & Continue')
