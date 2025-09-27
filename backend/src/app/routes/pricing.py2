from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Project, AuditLog
from ..ai_team.pricing_engine import PricingEngine
from ..ai_team.tech_recommender import TechRecommender
from ..ai_team.marketing_agent import MarketingAgent
from ..ai_team.security_auditor import SecurityAuditor
import logging

pricing_bp = Blueprint('pricing', __name__)
logger = logging.getLogger(__name__)

# Initialize AI team members
pricing_engine = PricingEngine()
tech_recommender = TechRecommender()
marketing_agent = MarketingAgent()
security_auditor = SecurityAuditor()

@pricing_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_project():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['description', 'project_type', 'complexity', 'timeline', 'team_size']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Use AI team to analyze project
        pricing_result = pricing_engine.calculate_price(data)
        tech_recommendations = tech_recommender.analyze(data)
        marketing_recommendations = marketing_agent.analyze(data)
        security_assessment = security_auditor.analyze(data)
        
        # Create project record
        project = Project(
            user_id=user_id,
            title=data.get('title', 'Untitled Project'),
            description=data['description'],
            project_type=data['project_type'],
            complexity=data['complexity'],
            timeline=data['timeline'],
            team_size=data['team_size'],
            estimated_price_zar=pricing_result['final_price_zar'],
            technical_recommendations=tech_recommendations,
            marketing_recommendations=marketing_recommendations,
            security_assessment=security_assessment,
            ai_confidence_score=pricing_result.get('confidence_score', 0.8)
        )
        
        db.session.add(project)
        db.session.commit()
        
        # Log pricing analysis
        from ..models import AuditLog
        AuditLog(
            user_id=user_id,
            action='PROJECT_ANALYZED',
            resource_type='PROJECT',
            resource_id=project.id,
            details={
                'project_type': data['project_type'],
                'estimated_price': pricing_result['final_price_zar'],
                'complexity': data['complexity']
            }
        )
        db.session.add(AuditLog)
        db.session.commit()
        
        return jsonify({
            'project_id': project.id,
            'pricing': pricing_result,
            'technical_recommendations': tech_recommendations,
            'marketing_recommendations': marketing_recommendations,
            'security_assessment': security_assessment,
            'ai_analysis': {
                'project_analyzer': 'Project requirements analyzed successfully',
                'tech_recommender': 'Technology stack recommended',
                'pricing_engine': 'Fair pricing calculated',
                'security_auditor': 'Security assessment completed',
                'marketing_agent': 'Marketing strategy prepared'
            }
        })
        
    except Exception as e:
        logger.error(f"Pricing analysis error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Project analysis failed'}), 500

@pricing_bp.route('/projects/<project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    try:
        user_id = get_jwt_identity()
        project = Project.query.filter_by(id=project_id, user_id=user_id).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({'project': project.to_dict()})
        
    except Exception as e:
        return jsonify({'error': 'Failed to get project'}), 500

@pricing_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_user_projects():
    try:
        user_id = get_jwt_identity()
        projects = Project.query.filter_by(user_id=user_id).order_by(Project.created_at.desc()).all()
        
        return jsonify({
            'projects': [project.to_dict() for project in projects]
        })
        
    except Exception as e:
        return jsonify({'error': 'Failed to get projects'}), 500
