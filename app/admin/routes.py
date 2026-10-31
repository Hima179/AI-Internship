from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from . import admin
from ..auth import role_required
from ..models import User, StudentProfile, AssessmentSession, AssessmentScore, Assessment, db
from sqlalchemy import or_
from datetime import datetime

@admin.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_counsellors = User.query.filter_by(role='counsellor').count()
    
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    completed_today = AssessmentSession.query.filter(AssessmentSession.completed_at >= today_start, AssessmentSession.status == 'completed').count()
    unassigned_students = StudentProfile.query.filter_by(assigned_counsellor_id=None).count()
    
    recent_completions = AssessmentSession.query.filter_by(status='completed').order_by(AssessmentSession.completed_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                           stats={
                               'total_students': total_students,
                               'total_counsellors': total_counsellors,
                               'completed_today': completed_today,
                               'unassigned_students': unassigned_students
                           },
                           recent_completions=recent_completions)

@admin.route('/students')
@login_required
@role_required('admin')
def students():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', 'all')
    
    query = User.query.filter_by(role='student').join(StudentProfile, User.id == StudentProfile.user_id)
    
    if search:
        query = query.filter(or_(User.name.contains(search), User.uai_id.contains(search)))
    
    if status == 'completed':
        query = query.filter(StudentProfile.id.in_(db.session.query(AssessmentSession.student_id).filter_by(status='completed')))
    elif status == 'pending':
        query = query.filter(~StudentProfile.id.in_(db.session.query(AssessmentSession.student_id).filter_by(status='completed')))
        
    pagination = query.paginate(page=page, per_page=20)
    student_list = pagination.items
    
    return render_template('admin/students.html', 
                           students=student_list, 
                           pagination=pagination, 
                           search=search, 
                           status=status)

@admin.route('/students/add', methods=['POST'])
@login_required
@role_required('admin')
def add_student():
    uai_id = request.form.get('uai_id')
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    department = request.form.get('department')
    
    if User.query.filter_by(uai_id=uai_id).first():
        flash('UAi ID already exists.', 'danger')
    else:
        new_user = User(uai_id=uai_id, name=name, email=email, role='student')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()
        
        new_profile = StudentProfile(user_id=new_user.id, department=department)
        db.session.add(new_profile)
        db.session.commit()
        flash(f'Student {name} added successfully.', 'success')
        
    return redirect(url_for('admin.students'))

@admin.route('/students/<int:user_id>/toggle', methods=['POST'])
@login_required
@role_required('admin')
def toggle_student(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({'success': True, 'is_active': user.is_active})

@admin.route('/counsellors')
@login_required
@role_required('admin')
def counsellors():
    counsellor_list = User.query.filter_by(role='counsellor').all()
    return render_template('admin/counsellors.html', counsellors=counsellor_list)

@admin.route('/assign')
@login_required
@role_required('admin')
def assign():
    unassigned = StudentProfile.query.filter_by(assigned_counsellor_id=None).all()
    counsellor_list = User.query.filter_by(role='counsellor').all()
    
    # Current assignments for display below
    current_assignments = StudentProfile.query.filter(StudentProfile.assigned_counsellor_id != None).all()
    
    return render_template('admin/assign.html', 
                           unassigned=unassigned, 
                           counsellors=counsellor_list,
                           current_assignments=current_assignments)

@admin.route('/assign', methods=['POST'])
@login_required
@role_required('admin')
def process_assign():
    student_ids = request.form.getlist('student_ids[]')
    counsellor_id = request.form.get('counsellor_id')
    
    if not student_ids or not counsellor_id:
        flash('Please select students and a counsellor.', 'warning')
        return redirect(url_for('admin.assign'))
    
    counsellor = User.query.get(counsellor_id)
    updated_count = 0
    for s_id in student_ids:
        profile = StudentProfile.query.get(s_id)
        if profile:
            profile.assigned_counsellor_id = counsellor_id
            updated_count += 1
            
    db.session.commit()
    flash(f'{updated_count} students assigned to {counsellor.name}.', 'success')
    return redirect(url_for('admin.assign'))


@admin.route('/counsellors/add', methods=['POST'])
@login_required
@role_required('admin')
def add_counsellor():
    uai_id  = request.form.get('uai_id', '').strip()
    name    = request.form.get('name', '').strip()
    email   = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if not uai_id or not name or not email or not password:
        flash('All fields are required.', 'danger')
        return redirect(url_for('admin.counsellors'))

    if User.query.filter_by(uai_id=uai_id).first():
        flash(f'UAI ID "{uai_id}" already exists.', 'danger')
        return redirect(url_for('admin.counsellors'))

    if User.query.filter_by(email=email).first():
        flash(f'Email "{email}" already in use.', 'danger')
        return redirect(url_for('admin.counsellors'))

    new_c = User(uai_id=uai_id, name=name, email=email, role='counsellor')
    new_c.set_password(password)
    db.session.add(new_c)
    db.session.commit()
    flash(f'Counsellor "{name}" added successfully!', 'success')
    return redirect(url_for('admin.counsellors'))


@admin.route('/counsellors/<int:user_id>/remove', methods=['POST'])
@login_required
@role_required('admin')
def remove_counsellor(user_id):
    c = User.query.get_or_404(user_id)
    if c.role != 'counsellor':
        flash('User is not a counsellor.', 'danger')
        return redirect(url_for('admin.counsellors'))

    # Unassign all students linked to this counsellor
    for profile in c.assigned_students:
        profile.assigned_counsellor_id = None

    db.session.delete(c)
    db.session.commit()
    flash(f'Counsellor "{c.name}" removed successfully.', 'success')
    return redirect(url_for('admin.counsellors'))

