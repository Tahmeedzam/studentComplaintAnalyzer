"""Integration tests for web routes, complaint lifecycle, and REST API endpoints."""

import pytest
from app import create_app
from app.models import db, User, Complaint


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # Seed test admin and test student
        admin = User(name="Admin User", email="admin@smartcampus.com", role="admin")
        admin.set_password("Admin@123")
        db.session.add(admin)

        student = User(name="Student User", email="student@smartcampus.com", role="student")
        student.set_password("Student@123")
        db.session.add(student)

        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_landing_page(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Smart Student Complaint Analyzer" in res.data


def test_api_analyze_endpoint(client):
    res = client.post('/api/analyze', json={
        "text": "The Wi-Fi in the library has not been working for two days."
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "category" in data
    assert "sentiment" in data
    assert "priority" in data
    assert "department" in data
    assert "keywords" in data


def test_complaint_submission_and_lifecycle(client, app):
    # Log in as student
    client.post('/login', data={
        'email': 'student@smartcampus.com',
        'password': 'Student@123'
    }, follow_redirects=True)

    # Submit complaint
    res = client.post('/student/complaints/new', data={
        'title': 'Library air conditioner broken',
        'description': 'The AC in the 2nd floor library reading room is broken and room is very hot.',
        'location': 'Library 2nd Floor'
    }, follow_redirects=True)
    assert res.status_code == 200

    # Verify in DB
    with app.app_context():
        complaint = Complaint.query.first()
        assert complaint is not None
        assert "Library" in complaint.title
        assert complaint.status == "Pending"
        assert complaint.category in {"Library", "Infrastructure", "Classroom", "Other"}

    # Log in as Admin and update status
    client.get('/logout', follow_redirects=True)
    client.post('/login', data={
        'email': 'admin@smartcampus.com',
        'password': 'Admin@123'
    }, follow_redirects=True)

    with app.app_context():
        c_id = Complaint.query.first().id

    update_res = client.post(f'/admin/complaints/{c_id}/update', data={
        'status': 'Resolved',
        'department': 'Maintenance Department',
        'admin_response': 'AC compressor was repaired and tested.'
    }, follow_redirects=True)
    assert update_res.status_code == 200

    with app.app_context():
        updated_c = db.session.get(Complaint, c_id)
        assert updated_c.status == "Resolved"
        assert "repaired" in updated_c.admin_response
