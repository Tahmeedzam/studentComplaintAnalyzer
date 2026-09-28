"""Student portal controller: Dashboard, Complaint Submission, Tracking, and Details."""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import db, Complaint
from app.utils import student_required
from ml.prediction import analyze_complaint

student_bp = Blueprint('student', __name__)


@student_bp.route('/dashboard')
@login_required
def dashboard():
    """Render the student dashboard with overview statistics and recent complaints."""
    user_id = current_user.id

    # Compute personal statistics
    total = Complaint.query.filter_by(student_id=user_id).count()
    pending = Complaint.query.filter_by(student_id=user_id, status='Pending').count()
    in_progress = Complaint.query.filter_by(student_id=user_id, status='In Progress').count()
    resolved = Complaint.query.filter_by(student_id=user_id, status='Resolved').count()

    recent_complaints = Complaint.query.filter_by(student_id=user_id)\
        .order_by(Complaint.created_at.desc())\
        .limit(5)\
        .all()

    return render_template(
        'student/dashboard.html',
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved,
        recent_complaints=recent_complaints
    )


@student_bp.route('/complaints/new', methods=['GET', 'POST'])
@login_required
def new_complaint():
    """Submit a new grievance with automatic real-time NLP classification & prioritization."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()

        if not title or not description:
            flash('Please provide both a title and a detailed description for your complaint.', 'warning')
            return render_template('student/new_complaint.html', title=title, description=description, location=location)

        # Full NLP Analysis Pipeline
        full_text = f"{title}. {description}" if location == "" else f"{title}. {description}. Location: {location}"
        analysis = analyze_complaint(full_text)

        # Create Complaint record in database
        complaint = Complaint(
            student_id=current_user.id,
            title=title,
            description=f"{description}\n\n[Location/Unit: {location}]" if location else description,
            category=analysis['category'],
            sentiment=analysis['sentiment'],
            sentiment_score=analysis['sentiment_score'],
            priority=analysis['priority'],
            department=analysis['department'],
            confidence=analysis['confidence'],
            status='Pending'
        )
        complaint.set_keywords(analysis['keywords'])

        db.session.add(complaint)
        db.session.commit()

        flash(f'Complaint #{complaint.id} successfully submitted and analyzed by NLP!', 'success')
        return redirect(url_for('student.complaint_detail', complaint_id=complaint.id))

    return render_template('student/new_complaint.html')


@student_bp.route('/complaints')
@login_required
def complaints():
    """List all complaints filed by the logged-in student with search & multi-filter support."""
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    priority = request.args.get('priority', '').strip()

    query = Complaint.query.filter_by(student_id=current_user.id)

    if search:
        query = query.filter(
            (Complaint.title.ilike(f'%{search}%')) |
            (Complaint.description.ilike(f'%{search}%'))
        )
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)

    complaint_list = query.order_by(Complaint.created_at.desc()).all()

    # Distinct categories for the filter dropdown
    categories = [
        "Academics", "Examination", "IT & Wi-Fi", "Infrastructure",
        "Classroom", "Library", "Canteen", "Hostel", "Transport",
        "Administration", "Fees & Accounts", "Other"
    ]

    return render_template(
        'student/complaints.html',
        complaints=complaint_list,
        categories=categories,
        search=search,
        selected_category=category,
        selected_status=status,
        selected_priority=priority
    )


@student_bp.route('/complaints/<int:complaint_id>')
@login_required
def complaint_detail(complaint_id):
    """View complete status history, NLP analytics breakdown, and admin response for a complaint."""
    complaint = db.session.get(Complaint, complaint_id)
    if not complaint:
        flash('Complaint not found.', 'warning')
        return redirect(url_for('student.dashboard'))

    # Security check: Ensure students can only view their own complaints
    if not current_user.is_admin and complaint.student_id != current_user.id:
        flash('You are not authorized to view this complaint.', 'danger')
        return redirect(url_for('student.dashboard'))

    return render_template('student/complaint_detail.html', complaint=complaint)
