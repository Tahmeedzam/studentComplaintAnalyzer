import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smartcampus-dev-key-college-mini-project-2026')
    
    # SQLAlchemy database configuration
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
    if db_url:
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        # Check if running in a serverless/read-only environment (e.g., Vercel / AWS Lambda)
        is_serverless = bool(os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))
        if is_serverless:
            sqlite_path = Path(tempfile.gettempdir()) / 'database.db'
        else:
            sqlite_path = BASE_DIR / 'instance' / 'database.db'
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Enable connection health check / pool pre-ping for cloud databases like Supabase
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # ML & Model Paths
    MODELS_DIR = BASE_DIR / 'models'
    DATA_DIR = BASE_DIR / 'data'
    MODEL_PATH = MODELS_DIR / 'complaint_classifier.pkl'
    VECTORIZER_PATH = MODELS_DIR / 'tfidf_vectorizer.pkl'
    DATASET_PATH = DATA_DIR / 'complaints_dataset.csv'

    # Safely ensure required runtime directories exist
    try:
        os.makedirs(BASE_DIR / 'instance', exist_ok=True)
        os.makedirs(MODELS_DIR, exist_ok=True)
        os.makedirs(DATA_DIR, exist_ok=True)
    except Exception:
        # Ignore on read-only serverless filesystems (e.g., Vercel)
        pass


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ENGINE_OPTIONS = {}
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
