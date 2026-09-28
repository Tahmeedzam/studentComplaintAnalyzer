"""Database models for Users and Student Complaints."""

from datetime import datetime, timezone
import json
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


def utc_now():
    """Return current UTC time."""
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    """User model representing students and administrative staff."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # 'student' | 'admin'
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationship to complaints submitted by this user
    complaints = db.relationship(
        'Complaint',
        backref='student',
        lazy=True,
        cascade="all, delete-orphan",
        order_by="desc(Complaint.created_at)"
    )

    def set_password(self, password: str):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password against stored hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        """Check if user has administrative privileges."""
        return self.role == 'admin'

    def to_dict(self) -> dict:
        """Convert user instance to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Complaint(db.Model):
    """Complaint model containing student grievances and ML/NLP analytical attributes."""
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # NLP & Machine Learning Derived Fields
    category = db.Column(db.String(80), nullable=False, default="Other")
    sentiment = db.Column(db.String(30), nullable=False, default="Neutral")  # 'Positive' | 'Neutral' | 'Negative'
    sentiment_score = db.Column(db.Float, nullable=False, default=0.0)
    priority = db.Column(db.String(20), nullable=False, default="Low")       # 'High' | 'Medium' | 'Low'
    department = db.Column(db.String(100), nullable=False, default="Administrative Office")
    confidence = db.Column(db.Float, nullable=False, default=0.0)
    keywords = db.Column(db.Text, nullable=True, default="[]")  # JSON-encoded list of keywords
    
    # Lifecycle & Resolution Fields
    status = db.Column(db.String(30), nullable=False, default="Pending")     # 'Pending' | 'In Progress' | 'Resolved' | 'Rejected'
    admin_response = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=utc_now, index=True)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    @property
    def keywords_list(self) -> list:
        """Retrieve keywords as Python list."""
        if not self.keywords:
            return []
        try:
            return json.loads(self.keywords)
        except Exception:
            return [k.strip() for k in self.keywords.split(',') if k.strip()]

    def set_keywords(self, kw_list: list):
        """Serialize keywords list to JSON string."""
        if isinstance(kw_list, list):
            self.keywords = json.dumps(kw_list)
        else:
            self.keywords = json.dumps([])

    def to_dict(self) -> dict:
        """Serialize complaint model to dictionary for REST API."""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.name if self.student else None,
            'student_email': self.student.email if self.student else None,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'sentiment': self.sentiment,
            'sentiment_score': round(self.sentiment_score, 2),
            'priority': self.priority,
            'department': self.department,
            'confidence': round(self.confidence, 1),
            'keywords': self.keywords_list,
            'status': self.status,
            'admin_response': self.admin_response,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

    def __repr__(self):
        return f"<Complaint #{self.id}: {self.title[:30]} ({self.status})>"
