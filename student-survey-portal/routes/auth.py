from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from models.user import db, User
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'student')
        
        if not username or not password:
            flash("Oops, looks like you forgot your username or password!", "error")
            if role == 'counsellor':
                return redirect(url_for('auth.counsellor_login'))
            elif role == 'faculty':
                return redirect(url_for('auth.faculty_login'))
            return redirect(url_for('auth.student_login'))

        # Verify against database
        user = User.query.filter_by(username=username, role=role).first()
        
        if user and user.check_password(password):
            login_user(user)
            logger.info(f"User '{username}' logged in successfully as '{role}'.")
            # Log them in based on role
            if role == 'student':
                flash(f"Welcome back, {username}!", "success")
                return redirect(url_for('survey.dashboard'))
            elif role == 'counsellor':
                flash("Counsellor dashboard accessed.", "success")
                return redirect(url_for('auth.counsellor'))
            else:
                flash("Faculty portal accessed.", "success")
                return redirect(url_for('auth.faculty'))
        else:
            logger.warning(f"Failed login attempt for username '{username}' with role '{role}'.")
            flash("Invalid Username or Password", "error")
            if role == 'counsellor':
                return redirect(url_for('auth.counsellor_login'))
            elif role == 'faculty':
                return redirect(url_for('auth.faculty_login'))
            return redirect(url_for('auth.student_login'))
            
    return redirect(url_for('auth.student_login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('auth.student_login'))

@auth_bp.route('/login/student', methods=['GET'])
def student_login():
    return render_template('student_login.html')

@auth_bp.route('/login/counsellor', methods=['GET'])
def counsellor_login():
    return render_template('counsellor_login.html')

@auth_bp.route('/login/faculty', methods=['GET'])
def faculty_login():
    return render_template('faculty_login.html')

from models.survey import SurveyResponse

@auth_bp.route('/faculty')
@login_required
def faculty():
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('auth.student_login'))
    
    responses = SurveyResponse.query.all()
    return render_template('faculty.html', responses=responses)

@auth_bp.route('/counsellor')
@login_required
def counsellor():
    if current_user.role != 'counsellor':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('auth.student_login'))
        
    responses = SurveyResponse.query.all()
    return render_template('counsellor.html', responses=responses)

# Temporary Registration Route to create users with hashed passwords
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'student')

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "error")
            return redirect(url_for('auth.register'))

        new_user = User(username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("User created successfully! You can now log in.", "success")
        return redirect(url_for('auth.student_login'))
        
    return '''
    <form method="POST" style="margin:50px auto; max-width: 300px; display:flex; flex-direction:column; gap:10px;">
        <h3>Register New User</h3>
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <select name="role">
            <option value="student">Student</option>
            <option value="counsellor">Counsellor</option>
            <option value="faculty">Faculty</option>
        </select>
        <button type="submit">Create User</button>
    </form>
    '''
