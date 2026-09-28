"""Utility functions, decorators, and Jinja helper filters."""

from functools import wraps
from flask import flash, redirect, url_for, abort, request, jsonify
from flask_login import current_user


def admin_required(f):
    """Decorator to enforce that the logged-in user has the admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required'}), 401
            flash('Please log in with an administrator account to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.is_admin:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Forbidden: Administrator privileges required'}), 403
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('student.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def student_required(f):
    """Decorator to enforce that the logged-in user is authenticated and is a student."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required'}), 401
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def format_priority_badge(priority: str) -> str:
    """Return Bootstrap badge class for priority levels."""
    mapping = {
        'High': 'badge-priority-high',
        'Medium': 'badge-priority-medium',
        'Low': 'badge-priority-low'
    }
    return mapping.get(priority, 'bg-secondary')


def format_status_badge(status: str) -> str:
    """Return Bootstrap badge class for complaint status."""
    mapping = {
        'Pending': 'badge-status-pending',
        'In Progress': 'badge-status-progress',
        'Resolved': 'badge-status-resolved',
        'Rejected': 'badge-status-rejected'
    }
    return mapping.get(status, 'bg-secondary')


def format_sentiment_badge(sentiment: str) -> str:
    """Return badge class for sentiment levels."""
    mapping = {
        'Positive': 'badge-sentiment-pos',
        'Neutral': 'badge-sentiment-neu',
        'Negative': 'badge-sentiment-neg'
    }
    return mapping.get(sentiment, 'bg-secondary')
