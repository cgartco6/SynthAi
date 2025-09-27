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

# Initialize AI team members with affordable pricing
pricing_engine = PricingEngine()
tech_recommender = TechRecommender()
marketing_agent = MarketingAgent()
security_auditor = SecurityAuditor()

@pricing_bp.route('/affordable-examples', methods=['GET'])
def get_affordable_examples():
    """Get examples of affordable project pricing"""
    examples = [
        {
            'type': 'simple_website',
            'name': 'Simple Website',
            'description': 'Basic landing page or portfolio website',
            'price_range': {'min': 5000, 'max': 15000},
            'timeline': '2-3 weeks',
            'features': ['Responsive design', 'Contact form', 'SEO basic']
        },
        {
            'type': 'ecommerce_basic',
            'name': 'Basic E-commerce Store',
            'description': 'Online store with essential features',
            'price_range': {'min': 15000, 'max': 40000},
            'timeline': '4-6 weeks',
            'features': ['Product catalog', 'Payment integration', 'Order management']
        },
        {
            'type': 'mobile_app',
            'name': 'Mobile Application',
            'description': 'Cross-platform mobile app',
            'price_range': {'min': 20000, 'max': 50000},
            'timeline': '6-8 weeks',
            'features': ['iOS & Android', 'Backend API', 'App store deployment']
        },
        {
            'type': 'business_software',
            'name': 'Business Management Software',
            'description': 'Custom business solution',
            'price_range': {'min': 25000, 'max': 80000},
            'timeline': '8-12 weeks',
            'features': ['Custom features', 'User management', 'Reporting']
        }
    ]
    
    return jsonify({'affordable_examples': examples})

@pricing_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_project():
    """Analyze project with affordable pricing"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['description', 'project_type', 'complexity', 'timeline', 'team_size']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Use AI team to analyze project with affordable pricing
        pricing_result = pricing_engine.calculate_price(data)
        tech_recommendations = tech_recommender.analyze(data)
        marketing_recommendations = marketing_agent.analyze(data)
        security_assessment = security_auditor.analyze(data)
        
        # Add affordable pricing message
        pricing_result['affordable_message'] = (
            "This quote uses our new affordable pricing model, specifically designed "
            "for South African businesses. Prices are 60% lower than our previous rates."
        )
        
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
        AuditLog(
            user_id=user_id,
            action='PROJECT_ANALYZED_AFFORDABLE',
            resource_type='PROJECT',
            resource_id=project.id,
            details={
                'project_type': data['project_type'],
                'estimated_price': pricing_result['final_price_zar'],
                'complexity': data['complexity'],
                'affordable_tier': True
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
                'project_analyzer': 'Project requirements analyzed with affordable pricing',
                'tech_recommender': 'Cost-effective technology stack recommended',
                'pricing_engine': 'Affordable pricing calculated for SA market',
                'security_auditor': 'Security assessment completed',
                'marketing_agent': 'Budget-friendly marketing strategy prepared'
            },
            'affordable_tier': True
        })
        
    except Exception as e:
        logger.error(f"Pricing analysis error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Project analysis failed'}), 500
