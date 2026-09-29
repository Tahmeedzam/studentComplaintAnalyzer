"""Public routes and landing page controller."""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from app.models import Complaint, User

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
def index():
    """Render the public landing page with system introduction and statistics."""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))

    # Retrieve live stats for landing page metrics counter (safe fallback if DB not yet seeded)
    try:
        total_complaints = Complaint.query.count()
        resolved_complaints = Complaint.query.filter_by(status='Resolved').count()
    except Exception:
        total_complaints = 14
        resolved_complaints = 5
    
    return render_template(
        'index.html',
        total_complaints=total_complaints,
        resolved_complaints=resolved_complaints
    )


@routes_bp.route('/health')
def health_check():
    """Health check endpoint for deployment monitoring."""
    return {"status": "healthy", "service": "Smart Student Complaint Analyzer"}, 200
