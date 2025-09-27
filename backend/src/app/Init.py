from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from celery import Celery
import os
import logging
from cryptography.fernet import Fernet

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
celery = Celery(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_mapping(
        # Security
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production'),
        
        # Database
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///synthai.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        
        # JWT
        JWT_ACCESS_TOKEN_EXPIRES=int(os.environ.get('JWT_EXPIRY_HOURS', 24)) * 3600,
        
        # Email
        MAIL_SERVER=os.environ.get('MAIL_SERVER', 'smtp.gmail.com'),
        MAIL_PORT=int(os.environ.get('MAIL_PORT', 587)),
        MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true',
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
        
        # Celery
        CELERY_BROKER_URL=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        CELERY_RESULT_BACKEND=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        
        # Encryption
        ENCRYPTION_KEY=os.environ.get('ENCRYPTION_KEY', Fernet.generate_key()),
        
        # Twilio (WhatsApp)
        TWILIO_ACCOUNT_SID=os.environ.get('TWILIO_ACCOUNT_SID'),
        TWILIO_AUTH_TOKEN=os.environ.get('TWILIO_AUTH_TOKEN'),
        TWILIO_WHATSAPP_NUMBER=os.environ.get('TWILIO_WHATSAPP_NUMBER'),
    )
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app, origins=os.environ.get('CORS_ORIGIN', 'http://localhost:3000'))
    
    # Configure Celery
    celery.conf.update(app.config)
    
    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.projects import projects_bp
    from .routes.pricing import pricing_bp
    from .routes.chatbot import chatbot_bp
    from .routes.payments import payments_bp
    from .routes.marketing import marketing_bp
    from .routes.whatsapp import whatsapp_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(pricing_bp, url_prefix='/api/pricing')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    app.register_blueprint(marketing_bp, url_prefix='/api/marketing')
    app.register_blueprint(whatsapp_bp, url_prefix='/api/whatsapp')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    logger.info("SynthAI application initialized successfully")
    return app

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery
