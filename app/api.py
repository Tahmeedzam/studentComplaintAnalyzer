"""REST API Endpoints for external integration, live frontend analysis, and complaint manipulation."""

from flask import Blueprint, request, jsonify
from flask_login import current_user
from app.models import db, Complaint, User
from app.utils import admin_required
from ml.prediction import analyze_complaint

api_bp = Blueprint('api', __name__)


@api_bp.route('/analyze', methods=['POST'])
def api_analyze_text():
    """
    NLP Analysis API Endpoint.
    Accepts JSON: {"text": "WiFi is not working in library"}
    Returns structured NLP inference results.
    """
    data = request.get_json(silent=True) or {}
    text = data.get('text', '').strip()

    if not text:
        return jsonify({
            'error': 'Missing required field: "text"'
        }), 400

    result = analyze_complaint(text)
    return jsonify(result), 200


@api_bp.route('/complaints', methods=['GET'])
def api_get_complaints():
    """Retrieve complaints list formatted in JSON."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized: Please log in'}), 401

    if current_user.is_admin:
        complaints_query = Complaint.query.order_by(Complaint.created_at.desc()).all()
    else:
        complaints_query = Complaint.query.filter_by(student_id=current_user.id)\
            .order_by(Complaint.created_at.desc()).all()

    return jsonify({
        'count': len(complaints_query),
        'complaints': [c.to_dict() for c in complaints_query]
    }), 200


@api_bp.route('/complaints/<int:complaint_id>', methods=['GET'])
def api_get_complaint(complaint_id):
    """Retrieve specific complaint by ID."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401

    complaint = db.session.get(Complaint, complaint_id)
    if not complaint:
        return jsonify({'error': 'Complaint not found'}), 404

    # Security check: Student can only access their own complaint
    if not current_user.is_admin and complaint.student_id != current_user.id:
        return jsonify({'error': 'Forbidden: Access denied'}), 403

    return jsonify(complaint.to_dict()), 200


@api_bp.route('/complaints', methods=['POST'])
def api_create_complaint():
    """Submit a complaint via REST API."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json(silent=True) or {}
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()

    if not title or not description:
        return jsonify({'error': 'Missing title or description'}), 400

    # Execute NLP analysis
    analysis = analyze_complaint(f"{title}. {description}")

    complaint = Complaint(
        student_id=current_user.id,
        title=title,
        description=description,
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

    return jsonify({
        'message': 'Complaint submitted successfully',
        'complaint': complaint.to_dict()
    }), 201


@api_bp.route('/complaints/<int:complaint_id>', methods=['PUT'])
def api_update_complaint(complaint_id):
    """Update complaint status or department (Admin only)."""
    if not current_user.is_authenticated or not current_user.is_admin:
        return jsonify({'error': 'Forbidden: Admin access required'}), 403

    complaint = db.session.get(Complaint, complaint_id)
    if not complaint:
        return jsonify({'error': 'Complaint not found'}), 404

    data = request.get_json(silent=True) or {}
    status = data.get('status')
    department = data.get('department')
    admin_response = data.get('admin_response')

    if status and status in {'Pending', 'In Progress', 'Resolved', 'Rejected'}:
        complaint.status = status
    if department:
        complaint.department = department
    if admin_response is not None:
        complaint.admin_response = admin_response

    db.session.commit()
    return jsonify({
        'message': 'Complaint updated successfully',
        'complaint': complaint.to_dict()
    }), 200


@api_bp.route('/complaints/<int:complaint_id>', methods=['DELETE'])
def api_delete_complaint(complaint_id):
    """Delete a complaint record (Admin only)."""
    if not current_user.is_authenticated or not current_user.is_admin:
        return jsonify({'error': 'Forbidden: Admin access required'}), 403

    complaint = db.session.get(Complaint, complaint_id)
    if not complaint:
        return jsonify({'error': 'Complaint not found'}), 404

    db.session.delete(complaint)
    db.session.commit()

    return jsonify({'message': f'Complaint #{complaint_id} deleted successfully'}), 200
