import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
import re
import json
from datetime import datetime

class ProjectPricingAI:
    """
    AI System for project pricing analysis
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.price_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        
        # South Africa specific factors
        self.zar_exchange_rate = 18.5  # USD to ZAR (example)
        self.sa_market_multiplier = 1.15  # SA market adjustment
        
        # AI Team members
        self.analyzers = {
            'project_analyzer': ProjectAnalyzer(),
            'tech_recommender': TechRecommender(),
            'pricing_engine': PricingEngine(),
            'security_auditor': SecurityAuditor(),
            'marketing_agent': MarketingAgent()
        }
    
    def train(self, historical_data):
        """
        Train the AI model on historical project data
        """
        try:
            # Prepare features
            texts = [item['description'] for item in historical_data]
            X_text = self.vectorizer.fit_transform(texts).toarray()
            
            # Numerical features
            X_num = np.array([
                [item['complexity'], item['team_size'], item['timeline']]
                for item in historical_data
            ])
            
            X = np.hstack([X_text, X_num])
            y = np.array([item['final_price'] for item in historical_data])
            
            # Train model
            self.price_model.fit(X, y)
            self.is_trained = True
            return True
        except Exception as e:
            print(f"Training error: {e}")
            return False
    
    def analyze_project(self, project_description, project_type, complexity, timeline, team_size):
        """
        Main method to analyze project and return pricing and recommendations
        """
        if not self.is_trained:
            return self._fallback_analysis(project_description, project_type, complexity, timeline, team_size)
        
        try:
            # Vectorize description
            desc_vector = self.vectorizer.transform([project_description]).toarray()
            
            # Create feature array
            features = np.hstack([
                desc_vector,
                np.array([[complexity, team_size, timeline]])
            ])
            
            # Get base prediction
            base_price = self.price_model.predict(features)[0]
            
            # Apply South Africa market adjustment
            zar_price = base_price * self.zar_exchange_rate * self.sa_market_multiplier
            
            # Get recommendations from AI team
            analysis = {
                'base_price_usd': round(base_price, 2),
                'final_price_zar': round(zar_price, 2),
                'analysis_date': datetime.now().isoformat(),
                'ai_team_recommendations': {}
            }
            
            # Get recommendations from each AI team member
            for role, analyzer in self.analyzers.items():
                analysis['ai_team_recommendations'][role] = analyzer.analyze(
                    project_description, project_type, complexity, timeline, team_size
                )
            
            return analysis
            
        except Exception as e:
            print(f"Analysis error: {e}")
            return self._fallback_analysis(project_description, project_type, complexity, timeline, team_size)
    
    def _fallback_analysis(self, project_description, project_type, complexity, timeline, team_size):
        """Fallback analysis when model isn't trained"""
        base_prices = {
            'web': 5000, 'mobile': 8000, 'ai': 15000, 
            'ecommerce': 10000, 'enterprise': 20000, 'other': 7000
        }
        
        complexity_mult = {'simple': 0.7, 'medium': 1.0, 'complex': 1.5, 'very-complex': 2.2}
        timeline_mult = {'flexible': 0.9, 'standard': 1.0, 'urgent': 1.3, 'asap': 1.7}
        team_mult = {'solo': 0.8, 'small': 1.0, 'medium': 1.3, 'large': 1.8}
        
        base_price = (base_prices.get(project_type, 7000) * 
                     complexity_mult.get(complexity, 1.0) * 
                     timeline_mult.get(timeline, 1.0) * 
                     team_mult.get(team_size, 1.0))
        
        zar_price = base_price * self.zar_exchange_rate * self.sa_market_multiplier
        
        return {
            'base_price_usd': round(base_price, 2),
            'final_price_zar': round(zar_price, 2),
            'analysis_date': datetime.now().isoformat(),
            'ai_team_recommendations': {
                'note': 'Using fallback pricing algorithm'
            }
        }


class ProjectAnalyzer:
    """AI for analyzing project requirements and complexity"""
    
    def analyze(self, description, project_type, complexity, timeline, team_size):
        word_count = len(description.split())
        tech_terms = len(re.findall(r'\b(API|database|cloud|mobile|web|AI|ML|blockchain)\b', description, re.IGNORECASE))
        
        complexity_score = (word_count * 0.1) + (tech_terms * 2) + {'simple': 1, 'medium': 3, 'complex': 6, 'very-complex': 10}[complexity]
        
        return {
            'complexity_score': round(complexity_score, 2),
            'estimated_timeline_weeks': max(2, complexity_score * 1.5),
            'key_requirements_identified': tech_terms,
            'risk_assessment': 'Low' if complexity_score < 10 else 'Medium' if complexity_score < 20 else 'High'
        }


class TechRecommender:
    """AI for recommending technologies"""
    
    def analyze(self, description, project_type, complexity, timeline, team_size):
        recommendations = {
            'web': ['React.js', 'Node.js', 'MongoDB', 'AWS'],
            'mobile': ['React Native', 'Firebase', 'iOS/Android Native'],
            'ai': ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn'],
            'ecommerce': ['Shopify', 'WooCommerce', 'Magento', 'Stripe'],
            'enterprise': ['Java Spring', '.NET', 'Oracle DB', 'Docker'],
            'other': ['JavaScript', 'Python', 'SQL', 'Cloud Services']
        }
        
        return {
            'recommended_tech_stack': recommendations.get(project_type, recommendations['other']),
            'scalability_recommendations': 'Microservices architecture' if complexity in ['complex', 'very-complex'] else 'Monolithic architecture',
            'sa_specific_recommendations': ['Local hosting options', 'Payment gateways supporting ZAR', 'SA compliance standards']
        }


class PricingEngine:
    """AI for calculating fair pricing"""
    
    def analyze(self, description, project_type, complexity, timeline, team_size):
        base_rates = {
            'web': 850, 'mobile': 1100, 'ai': 1500, 
            'ecommerce': 950, 'enterprise': 1200, 'other': 800
        }
        
        rate = base_rates.get(project_type, 800)
        urgency_multiplier = 1.0 if timeline in ['flexible', 'standard'] else 1.5
        
        return {
            'hourly_rate_zar': rate,
            'estimated_hours': {'simple': 80, 'medium': 160, 'complex': 320, 'very-complex': 640}[complexity],
            'urgency_multiplier': urgency_multiplier,
            'payment_terms': ['50% upfront, 50% on completion', 'Monthly milestones', 'ZAR payments only']
        }


class SecurityAuditor:
    """AI for security recommendations"""
    
    def analyze(self, description, project_type, complexity, timeline, team_size):
        security_level = 'Standard' if complexity in ['simple', 'medium'] else 'Advanced' if complexity == 'complex' else 'Military'
        
        return {
            'recommended_security_level': security_level,
            'encryption_standards': ['AES-256', 'TLS 1.3', 'End-to-end encryption'],
            'compliance_frameworks': ['POPIA (SA)', 'GDPR', 'ISO 27001'],
            'security_testing': ['Penetration testing', 'Code review', 'Vulnerability assessment']
        }


class MarketingAgent:
    """AI for marketing strategy"""
    
    def analyze(self, description, project_type, complexity, timeline, team_size):
        platforms = {
            'web': ['Google Ads', 'Facebook', 'LinkedIn', 'Twitter'],
            'mobile': ['App Store Optimization', 'TikTok', 'Instagram', 'YouTube'],
            'ai': ['LinkedIn', 'Tech blogs', 'Industry forums', 'Research publications'],
            'ecommerce': ['Instagram Shopping', 'Facebook Marketplace', 'Influencer marketing', 'Email campaigns'],
            'enterprise': ['LinkedIn', 'Industry events', 'Whitepapers', 'Webinars'],
            'other': ['Multi-channel approach', 'Content marketing', 'Social media advertising']
        }
        
        return {
            'recommended_platforms': platforms.get(project_type, platforms['other']),
            'sa_specific_strategies': ['Local SEO for South Africa', 'SA social media trends', 'Local influencer partnerships'],
            'content_recommendations': ['Case studies', 'Demo videos', 'Testimonials', 'Blog posts'],
            'budget_allocation_zar': {'simple': 5000, 'medium': 15000, 'complex': 35000, 'very-complex': 70000}[complexity]
        }


# Example usage
if __name__ == "__main__":
    # Initialize AI system
    ai_system = ProjectPricingAI()
    
    # Sample historical data for training
    historical_projects = [
        {
            'description': 'E-commerce website with payment integration',
            'project_type': 'ecommerce',
            'complexity': 2,
            'team_size': 2,
            'timeline': 2,
            'final_price': 12000
        },
        # Add more historical data here
    ]
    
    # Train the AI
    if historical_projects:
        ai_system.train(historical_projects)
    
    # Analyze a new project
    project_analysis = ai_system.analyze_project(
        project_description="Mobile app for food delivery service with real-time tracking",
        project_type="mobile",
        complexity="complex",
        timeline="urgent",
        team_size="medium"
    )
    
    print("AI Project Analysis Results:")
    print(json.dumps(project_analysis, indent=2))
