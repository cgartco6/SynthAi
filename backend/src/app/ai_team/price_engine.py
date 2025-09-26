import os
import logging
from typing import Dict, Any
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

logger = logging.getLogger(__name__)

class PricingEngine:
    def __init__(self):
        self.model = None
        self.features = [
            'project_type', 'complexity', 'timeline', 'team_size', 
            'description_length', 'tech_terms_count'
        ]
        self.load_model()
    
    def load_model(self):
        """Load pre-trained pricing model"""
        try:
            # In production, this would load from a model registry
            self.model = self._train_default_model()
            logger.info("Pricing model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading pricing model: {e}")
            self.model = self._train_default_model()
    
    def _train_default_model(self):
        """Train a default model with sample data"""
        # Sample training data (in production, this would come from historical data)
        sample_data = {
            'project_type': ['web', 'mobile', 'ai', 'ecommerce', 'enterprise'] * 20,
            'complexity': ['simple', 'medium', 'complex', 'very-complex'] * 25,
            'timeline': ['flexible', 'standard', 'urgent', 'asap'] * 25,
            'team_size': ['solo', 'small', 'medium', 'large'] * 25,
            'description_length': np.random.randint(100, 2000, 100),
            'tech_terms_count': np.random.randint(1, 20, 100),
            'price': np.random.uniform(5000, 100000, 100)
        }
        
        df = pd.DataFrame(sample_data)
        X = pd.get_dummies(df[self.features[:-2]], drop_first=True)
        X['description_length'] = df['description_length']
        X['tech_terms_count'] = df['tech_terms_count']
        y = df['price']
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model
    
    def calculate_price(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate project price using AI model"""
        try:
            # Extract features
            features = self._extract_features(project_data)
            
            # Make prediction
            price_prediction = self.model.predict([features])[0]
            
            # Apply South Africa market adjustment
            zar_price = price_prediction * 1.15  # Market adjustment factor
            
            # Round to nearest 100
            final_price = round(zar_price / 100) * 100
            
            return {
                'base_price_usd': round(price_prediction, 2),
                'final_price_zar': final_price,
                'confidence_score': 0.85,
                'price_breakdown': self._generate_price_breakdown(project_data, final_price)
            }
            
        except Exception as e:
            logger.error(f"Error calculating price: {e}")
            return self._fallback_calculation(project_data)
    
    def _extract_features(self, project_data: Dict[str, Any]) -> list:
        """Extract features for the model"""
        # This would be more sophisticated in production
        description = project_data.get('description', '')
        project_type = project_data.get('project_type', 'other')
        complexity = project_data.get('complexity', 'medium')
        timeline = project_data.get('timeline', 'standard')
        team_size = project_data.get('team_size', 'small')
        
        # Create feature vector
        features = []
        
        # Project type encoding (simplified)
        type_mapping = {'web': 0, 'mobile': 1, 'ai': 2, 'ecommerce': 3, 'enterprise': 4, 'other': 5}
        features.extend([1 if i == type_mapping.get(project_type, 5) else 0 
                        for i in range(6)])
        
        # Complexity encoding
        complexity_mapping = {'simple': 0, 'medium': 1, 'complex': 2, 'very-complex': 3}
        features.extend([1 if i == complexity_mapping.get(complexity, 1) else 0 
                        for i in range(4)])
        
        # Timeline encoding
        timeline_mapping = {'flexible': 0, 'standard': 1, 'urgent': 2, 'asap': 3}
        features.extend([1 if i == timeline_mapping.get(timeline, 1) else 0 
                        for i in range(4)])
        
        # Team size encoding
        team_mapping = {'solo': 0, 'small': 1, 'medium': 2, 'large': 3}
        features.extend([1 if i == team_mapping.get(team_size, 1) else 0 
                        for i in range(4)])
        
        # Text features
        features.append(len(description))
        features.append(len([word for word in description.lower().split() 
                           if word in ['api', 'database', 'cloud', 'mobile', 'web', 'ai', 'ml']]))
        
        return features
    
    def _generate_price_breakdown(self, project_data: Dict[str, Any], total_price: float) -> Dict[str, float]:
        """Generate detailed price breakdown"""
        breakdown = {
            'development': total_price * 0.6,
            'project_management': total_price * 0.15,
            'quality_assurance': total_price * 0.1,
            'deployment': total_price * 0.1,
            'support_maintenance': total_price * 0.05
        }
        return breakdown
    
    def _fallback_calculation(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback pricing calculation"""
        base_prices = {
            'web': 85000, 'mobile': 135000, 'ai': 255000, 
            'ecommerce': 170000, 'enterprise': 340000, 'other': 119000
        }
        
        complexity_mult = {'simple': 0.7, 'medium': 1.0, 'complex': 1.5, 'very-complex': 2.2}
        timeline_mult = {'flexible': 0.9, 'standard': 1.0, 'urgent': 1.3, 'asap': 1.7}
        team_mult = {'solo': 0.8, 'small': 1.0, 'medium': 1.3, 'large': 1.8}
        
        base_price = base_prices.get(project_data.get('project_type', 'other'), 119000)
        price = base_price * complexity_mult.get(project_data.get('complexity', 'medium'), 1.0)
        price *= timeline_mult.get(project_data.get('timeline', 'standard'), 1.0)
        price *= team_mult.get(project_data.get('team_size', 'small'), 1.0)
        
        return {
            'base_price_usd': round(price / 18.5, 2),  # Approximate USD conversion
            'final_price_zar': round(price / 100) * 100,
            'confidence_score': 0.7,
            'price_breakdown': self._generate_price_breakdown(project_data, price)
        }
