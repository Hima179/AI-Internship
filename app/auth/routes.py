from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegisterForm
from ..models import User, StudentProfile, db

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            profile = current_user.student_profile
            if not profile or not profile.consent_given:
                return redirect(url_for('student.consent'))
            elif not profile.age or not profile.department:
                return redirect(url_for('student.details'))
            return redirect(url_for('student.dashboard'))
        return redirect(url_for(f'{current_user.role}.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            uai_id=form.uai_id.data,
            name=form.name.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush() # To get user.id for StudentProfile if needed
        
        if user.role == 'student':
            profile = StudentProfile(user_id=user.id)
            db.session.add(profile)
            
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            profile = current_user.student_profile
            if not profile or not profile.consent_given:
                return redirect(url_for('student.consent'))
            elif not profile.age or not profile.department:
                return redirect(url_for('student.details'))
            return redirect(url_for('student.dashboard'))
        elif current_user.role == 'counsellor':
            return redirect(url_for('counsellor.dashboard'))
        elif current_user.role == 'faculty':
            return redirect(url_for('faculty.dashboard'))
            
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.uai_id == form.uai_id.data) | (User.email == form.uai_id.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                if user.role == 'student':
                    profile = user.student_profile
                    if not profile or not profile.consent_given:
                        next_page = url_for('student.consent')
                    elif not profile.age or not profile.department:
                        next_page = url_for('student.details')
                    else:
                        next_page = url_for('student.dashboard')
                elif user.role == 'counsellor':
                    next_page = url_for('counsellor.dashboard')
                elif user.role == 'admin':
                    next_page = url_for('admin.dashboard')
                else:
                    next_page = url_for('faculty.dashboard')
            return redirect(next_page)
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
