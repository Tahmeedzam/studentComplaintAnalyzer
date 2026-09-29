"""Authentication controller: Registration, Login, and Session Termination."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user authentication for students and administrators."""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        if not email or not password:
            flash('Please enter both email address and password.', 'warning')
            return render_template('login.html', email=email)

        try:
            user = User.query.filter_by(email=email).first()
        except Exception as e:
            flash(f'Database connection error: Unable to authenticate. Please check database settings or try again.', 'danger')
            return render_template('login.html', email=email)

        if not user or not user.check_password(password):
            flash('Invalid email or password. Please verify your credentials.', 'danger')
            return render_template('login.html', email=email)

        login_user(user, remember=remember)
        flash(f'Welcome back, {user.name}!', 'success')

        # Redirect to intended next url or role dashboard
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)

        if user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new student account registration."""
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validations
        if not name or not email or not password:
            flash('All required fields must be filled.', 'warning')
            return render_template('register.html', name=name, email=email)

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'warning')
            return render_template('register.html', name=name, email=email)

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return render_template('register.html', name=name, email=email)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email address already exists. Please log in.', 'info')
            return redirect(url_for('auth.login'))

        # Create new student account
        new_student = User(
            name=name,
            email=email,
            role='student'
        )
        new_student.set_password(password)

        db.session.add(new_student)
        db.session.commit()

        login_user(new_student)
        flash('Account registered successfully! Welcome to SmartCampus.', 'success')
        return redirect(url_for('student.dashboard'))

    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Terminate current user session."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('routes.index'))
