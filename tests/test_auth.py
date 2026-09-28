"""Unit and integration tests for user authentication and Role-Based Access Control."""

import pytest
from app import create_app
from app.models import db, User


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # Seed test admin and test student
        admin = User(name="Test Admin", email="admin_test@test.com", role="admin")
        admin.set_password("AdminPass123")
        db.session.add(admin)

        student = User(name="Test Student", email="student_test@test.com", role="student")
        student.set_password("StudentPass123")
        db.session.add(student)

        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_password_hashing():
    user = User(name="Demo", email="demo@test.com", role="student")
    user.set_password("Secret123")
    assert user.password_hash != "Secret123"
    assert user.check_password("Secret123") is True
    assert user.check_password("WrongPass") is False


def test_user_roles(app):
    with app.app_context():
        admin = User.query.filter_by(email="admin_test@test.com").first()
        student = User.query.filter_by(email="student_test@test.com").first()

        assert admin.is_admin is True
        assert student.is_admin is False


def test_login_success(client):
    res = client.post('/login', data={
        'email': 'student_test@test.com',
        'password': 'StudentPass123'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Student Dashboard" in res.data or b"Dashboard" in res.data


def test_login_invalid_password(client):
    res = client.post('/login', data={
        'email': 'student_test@test.com',
        'password': 'WrongPassword'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Invalid email or password" in res.data


def test_student_registration(client, app):
    res = client.post('/register', data={
        'name': 'New Student',
        'email': 'new_student@test.com',
        'password': 'Password123',
        'confirm_password': 'Password123'
    }, follow_redirects=True)
    assert res.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email="new_student@test.com").first()
        assert user is not None
        assert user.role == "student"


def test_admin_route_protection_for_students(client):
    # Log in as student
    client.post('/login', data={
        'email': 'student_test@test.com',
        'password': 'StudentPass123'
    }, follow_redirects=True)

    # Attempt to visit admin dashboard
    res = client.get('/admin/dashboard', follow_redirects=True)
    assert res.status_code == 200
    assert b"Access denied" in res.data or b"Student Dashboard" in res.data
