from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Student

bp = Blueprint('main', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check for missing fields (Acceptance Criterion 2)
        if not student_id or not full_name or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html'), 400

        # Check for duplicate student ID or email (Acceptance Criterion 3)
        student = Student.query.filter((Student.student_id == student_id) | (Student.email == email)).first()
        if student:
            flash('Student ID or email already registered.', 'error')
            return render_template('register.html'), 400

        # Validate email format (Basic check, could be more robust)
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'error')
            return render_template('register.html'), 400

        # Create new student account (Acceptance Criterion 1)
        new_student = Student(
            student_id=student_id,
            full_name=full_name,
            email=email,
            password_hash=None  # Will be set by set_password
        )
        new_student.set_password(password)
        db.session.add(new_student)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.index')) # Assuming 'index' route exists or redirect to a home page

    return render_template('register.html')