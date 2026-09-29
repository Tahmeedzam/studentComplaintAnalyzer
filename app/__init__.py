"""Flask Application Factory and Extensions Initialization."""

import os
from pathlib import Path
from flask import Flask, render_template, jsonify
from flask_login import LoginManager
from flask_cors import CORS
from config import config_by_name
from app.models import db, User
from app.utils import format_priority_badge, format_status_badge, format_sentiment_badge

login_manager = LoginManager()


def create_app(config_name=None):
    """Application factory for Smart Student Complaint Analyzer."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'production')

    base_dir = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        template_folder=str(base_dir / 'templates'),
        static_folder=str(base_dir / 'static')
    )
    
    # Load configuration
    app_config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(app_config)

    # Initialize Extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except Exception:
            return None

    # Register Jinja context filters & global helpers
    app.jinja_env.filters['priority_badge'] = format_priority_badge
    app.jinja_env.filters['status_badge'] = format_status_badge
    app.jinja_env.filters['sentiment_badge'] = format_sentiment_badge

    # Register Blueprints
    from app.routes import routes_bp
    from app.auth import auth_bp
    from app.student import student_bp
    from app.admin import admin_bp
    from app.api import api_bp

    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(e):
        return render_template('404.html', message="Access Forbidden"), 403

    # Initialize tables and ensure admin user exists in production/development
    if not app.config.get('TESTING'):
        with app.app_context():
            try:
                db.create_all()
                if not User.query.filter_by(email='admin@smartcampus.com').first():
                    admin = User(
                        name="Campus Administrator",
                        email="admin@smartcampus.com",
                        role="admin"
                    )
                    admin.set_password("Admin@123")
                    db.session.add(admin)
                    
                    demo_student = User(
                        name="Aarav Sharma",
                        email="student@smartcampus.com",
                        role="student"
                    )
                    demo_student.set_password("Student@123")
                    db.session.add(demo_student)
                    
                    db.session.commit()
            except Exception as e:
                app.logger.warning(f"Database table initialization warning: {e}")
            
    return app
