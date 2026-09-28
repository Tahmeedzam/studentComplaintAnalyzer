"""Administrator portal controller: Dashboard, Complaint Management, Analytics, and Settings."""

from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import db, User, Complaint
from app.utils import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Render administrative command dashboard with live aggregated KPIs and charts."""
    total = Complaint.query.count()
    pending = Complaint.query.filter_by(status='Pending').count()
    in_progress = Complaint.query.filter_by(status='In Progress').count()
    resolved = Complaint.query.filter_by(status='Resolved').count()
    high_priority = Complaint.query.filter_by(priority='High').count()

    # Category aggregation for Chart.js
    category_counts = db.session.query(
        Complaint.category, func.count(Complaint.id)
    ).group_by(Complaint.category).all()
    
    # Sentiment aggregation
    sentiment_counts = db.session.query(
        Complaint.sentiment, func.count(Complaint.id)
    ).group_by(Complaint.sentiment).all()

    # Priority aggregation
    priority_counts = db.session.query(
        Complaint.priority, func.count(Complaint.id)
    ).group_by(Complaint.priority).all()

    # Status aggregation
    status_counts = db.session.query(
        Complaint.status, func.count(Complaint.id)
    ).group_by(Complaint.status).all()

    recent_complaints = Complaint.query\
        .order_by(Complaint.created_at.desc())\
        .limit(8)\
        .all()

    return render_template(
        'admin/dashboard.html',
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved,
        high_priority=high_priority,
        category_data=dict(category_counts),
        sentiment_data=dict(sentiment_counts),
        priority_data=dict(priority_counts),
        status_data=dict(status_counts),
        recent_complaints=recent_complaints
    )


@admin_bp.route('/complaints')
@login_required
@admin_required
def complaints():
    """Manage, search, and filter all complaints submitted across the institution."""
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    priority = request.args.get('priority', '').strip()
    status = request.args.get('status', '').strip()
    sentiment = request.args.get('sentiment', '').strip()
    department = request.args.get('department', '').strip()

    query = Complaint.query

    if search:
        query = query.join(User).filter(
            (Complaint.title.ilike(f'%{search}%')) |
            (Complaint.description.ilike(f'%{search}%')) |
            (User.name.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )
    if category:
        query = query.filter(Complaint.category == category)
    if priority:
        query = query.filter(Complaint.priority == priority)
    if status:
        query = query.filter(Complaint.status == status)
    if sentiment:
        query = query.filter(Complaint.sentiment == sentiment)
    if department:
        query = query.filter(Complaint.department == department)

    complaint_list = query.order_by(Complaint.created_at.desc()).all()

    # Distinct categories and departments for filter dropdowns
    categories = [
        "Academics", "Examination", "IT & Wi-Fi", "Infrastructure",
        "Classroom", "Library", "Canteen", "Hostel", "Transport",
        "Administration", "Fees & Accounts", "Other"
    ]
    departments = [
        "Academic Department", "Examination Cell", "IT Support",
        "Maintenance Department", "Administration", "Library Department",
        "Canteen Management", "Hostel Administration", "Transport Department",
        "Accounts Department", "Administrative Office", "General Administration"
    ]

    return render_template(
        'admin/complaints.html',
        complaints=complaint_list,
        categories=categories,
        departments=departments,
        search=search,
        selected_category=category,
        selected_priority=priority,
        selected_status=status,
        selected_sentiment=sentiment,
        selected_department=department
    )


@admin_bp.route('/complaints/<int:complaint_id>')
@login_required
@admin_required
def complaint_detail(complaint_id):
    """View detailed grievance information and administer response actions."""
    complaint = db.session.get(Complaint, complaint_id)
    if not complaint:
        flash('Complaint not found', 'danger')
        return redirect(url_for('admin.complaints'))

    departments = [
        "Academic Department", "Examination Cell", "IT Support",
        "Maintenance Department", "Administration", "Library Department",
        "Canteen Management", "Hostel Administration", "Transport Department",
        "Accounts Department", "Administrative Office", "General Administration"
    ]
    return render_template('admin/complaint_detail.html', complaint=complaint, departments=departments)


@admin_bp.route('/complaints/<int:complaint_id>/update', methods=['POST'])
@login_required
@admin_required
def update_complaint(complaint_id):
    """Update complaint status, assigned department, or official admin response."""
    complaint = db.session.get(Complaint, complaint_id)
    if not complaint:
        flash('Complaint not found', 'danger')
        return redirect(url_for('admin.complaints'))

    new_status = request.form.get('status', complaint.status)
    new_department = request.form.get('department', complaint.department)
    admin_response = request.form.get('admin_response', '').strip()

    valid_statuses = {'Pending', 'In Progress', 'Resolved', 'Rejected'}
    if new_status in valid_statuses:
        complaint.status = new_status

    if new_department:
        complaint.department = new_department

    if admin_response:
        complaint.admin_response = admin_response

    complaint.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    flash(f'Complaint #{complaint.id} updated successfully.', 'success')
    return redirect(url_for('admin.complaint_detail', complaint_id=complaint.id))


@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """Render comprehensive analytical reports and trend charts with time window filtering."""
    time_filter = request.args.get('time_filter', 'all')
    
    query = Complaint.query
    now = datetime.now(timezone.utc)

    if time_filter == '7days':
        query = query.filter(Complaint.created_at >= now - timedelta(days=7))
    elif time_filter == '30days':
        query = query.filter(Complaint.created_at >= now - timedelta(days=30))
    elif time_filter == '3months':
        query = query.filter(Complaint.created_at >= now - timedelta(days=90))

    filtered_complaints = query.all()
    total_count = len(filtered_complaints)

    if total_count > 0:
        resolved_count = sum(1 for c in filtered_complaints if c.status == 'Resolved')
        resolution_rate = round((resolved_count / total_count) * 100, 1)

        negative_count = sum(1 for c in filtered_complaints if c.sentiment == 'Negative')
        negative_pct = round((negative_count / total_count) * 100, 1)

        high_priority_count = sum(1 for c in filtered_complaints if c.priority == 'High')

        # Most common category
        cat_freq = {}
        for c in filtered_complaints:
            cat_freq[c.category] = cat_freq.get(c.category, 0) + 1
        most_common_category = max(cat_freq, key=cat_freq.get) if cat_freq else "N/A"

        # Most common department
        dept_freq = {}
        for c in filtered_complaints:
            dept_freq[c.department] = dept_freq.get(c.department, 0) + 1
        most_common_dept = max(dept_freq, key=dept_freq.get) if dept_freq else "N/A"
    else:
        resolution_rate = 0.0
        negative_pct = 0.0
        high_priority_count = 0
        most_common_category = "N/A"
        most_common_dept = "N/A"

    # Category counts for chart
    category_chart = {}
    sentiment_chart = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    priority_chart = {'High': 0, 'Medium': 0, 'Low': 0}

    for c in filtered_complaints:
        category_chart[c.category] = category_chart.get(c.category, 0) + 1
        sentiment_chart[c.sentiment] = sentiment_chart.get(c.sentiment, 0) + 1
        priority_chart[c.priority] = priority_chart.get(c.priority, 0) + 1

    return render_template(
        'admin/analytics.html',
        time_filter=time_filter,
        total_count=total_count,
        resolution_rate=resolution_rate,
        negative_pct=negative_pct,
        high_priority_count=high_priority_count,
        most_common_category=most_common_category,
        most_common_dept=most_common_dept,
        category_chart=category_chart,
        sentiment_chart=sentiment_chart,
        priority_chart=priority_chart
    )


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    """Allow administrative users to manage their account details and credentials."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not name or not email:
            flash('Name and email cannot be empty.', 'warning')
            return redirect(url_for('admin.settings'))

        # Check email uniqueness if modified
        if email != current_user.email:
            existing = User.query.filter_by(email=email).first()
            if existing:
                flash('This email address is already in use.', 'danger')
                return redirect(url_for('admin.settings'))
            current_user.email = email

        current_user.name = name

        if new_password:
            if len(new_password) < 6:
                flash('New password must be at least 6 characters long.', 'warning')
                return redirect(url_for('admin.settings'))
            if new_password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('admin.settings'))
            current_user.set_password(new_password)

        db.session.commit()
        flash('Account settings updated successfully.', 'success')
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html')
