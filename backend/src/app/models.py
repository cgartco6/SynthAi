from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import uuid
import json

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    
    # Security fields
    mfa_enabled = db.Column(db.Boolean, default=False)
    mfa_secret = db.Column(db.String(32))
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime)
    
    # Relationships
    projects = db.relationship('Project', backref='user', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='user', lazy=True)
    marketing_campaigns = db.relationship('MarketingCampaign', backref='user', lazy=True)
    chat_sessions = db.relationship('ChatSession', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def increment_failed_login(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.account_locked_until = datetime.utcnow() + timedelta(minutes=30)
    
    def reset_login_attempts(self):
        self.failed_login_attempts = 0
        self.account_locked_until = None
    
    def is_account_locked(self):
        if self.account_locked_until and datetime.utcnow() < self.account_locked_until:
            return True
        return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company': self.company,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'is_verified': self.is_verified,
            'mfa_enabled': self.mfa_enabled
        }

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    project_type = db.Column(db.String(50), nullable=False)
    complexity = db.Column(db.String(20), nullable=False)
    timeline = db.Column(db.String(20), nullable=False)
    team_size = db.Column(db.String(20), nullable=False)
    
    # AI Analysis Results
    estimated_price_zar = db.Column(db.Float, nullable=False)
    technical_recommendations = db.Column(db.JSON)
    marketing_recommendations = db.Column(db.JSON)
    security_assessment = db.Column(db.JSON)
    ai_confidence_score = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='project', lazy=True)
    marketing_campaigns = db.relationship('MarketingCampaign', backref='project', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'project_type': self.project_type,
            'complexity': self.complexity,
            'timeline': self.timeline,
            'team_size': self.team_size,
            'estimated_price_zar': self.estimated_price_zar,
            'technical_recommendations': self.technical_recommendations,
            'marketing_recommendations': self.marketing_recommendations,
            'security_assessment': self.security_assessment,
            'ai_confidence_score': self.ai_confidence_score,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    amount_zar = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='ZAR')
    stripe_payment_intent_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Encrypted bank details for South African banks
    bank_account_number = db.Column(db.String(50))  # Encrypted
    bank_name = db.Column(db.String(100))
    branch_code = db.Column(db.String(10))

class MarketingCampaign(db.Model):
    __tablename__ = 'marketing_campaigns'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    budget_zar = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='active')
    targeting_parameters = db.Column(db.JSON)
    performance_metrics = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    session_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), index=True)
    action = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.String(36))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
