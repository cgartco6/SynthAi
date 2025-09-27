import os
import logging
from typing import Dict, Any
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import openai

logger = logging.getLogger(__name__)

class PricingEngine:
    def __init__(self):
        self.model = None
        self.openai_client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.load_model()
    
    def load_model(self):
        """Load or train pricing model"""
        try:
            model_path = 'models/pricing_model.pkl'
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info("Pricing model loaded from file")
            else:
                self.model = self._train_model()
                os.makedirs('models', exist_ok=True)
                joblib.dump(self.model, model_path)
                logger.info("Pricing model trained and saved")
        except Exception as e:
            logger.error(f"Error loading pricing model: {e}")
            self.model = self._train_fallback_model()
    
    def _train_model(self):
        """Train model with historical data"""
        # This would connect to your historical data in production
        # For now, using enhanced sample data
        sample_data = self._generate_training_data()
        df = pd.DataFrame(sample_data)
        
        # Feature engineering
        X = self._engineer_features(df)
        y = df['price']
        
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        model.fit(X, y)
        return model
    
    def _generate_training_data(self):
        """Generate realistic training data for South African market"""
        project_types = ['web', 'mobile', 'ai', 'ecommerce', 'enterprise', 'other']
        complexities = ['simple', 'medium', 'complex', 'very-complex']
        timelines = ['flexible', 'standard', 'urgent', 'asap']
        team_sizes = ['solo', 'small', 'medium', 'large']
        
        data = []
        base_prices = {
            'web': 85000, 'mobile': 135000, 'ai': 255000, 
            'ecommerce': 170000, 'enterprise': 340000, 'other': 119000
        }
        
        for _ in range(1000):
            project_type = np.random.choice(project_types)
            complexity = np.random.choice(complexities)
            timeline = np.random.choice(timelines)
            team_size = np.random.choice(team_sizes)
            
            base_price = base_prices[project_type]
            
            # Apply multipliers with some randomness
            complexity_mult = {'simple': 0.7, 'medium': 1.0, 'complex': 1.8, 'very-complex': 2.5}
            timeline_mult = {'flexible': 0.9, 'standard': 1.0, 'urgent': 1.4, 'asap': 2.0}
            team_mult = {'solo': 0.8, 'small': 1.0, 'medium': 1.5, 'large': 2.2}
            
            price = base_price * complexity_mult[complexity]
            price *= timeline_mult[timeline] * team_mult[team_size]
            
            # Add noise and market variations
            price *= np.random.uniform(0.9, 1.1)
            
            data.append({
                'project_type': project_type,
                'complexity': complexity,
                'timeline': timeline,
                'team_size': team_size,
                'description_length': np.random.randint(50, 2000),
                'tech_terms_count': np.random.randint(1, 15),
                'price': price
            })
        
        return data
    
    def _engineer_features(self, df):
        """Engineer features for the model"""
        # Convert categorical variables to numerical
        type_mapping = {t: i for i, t in enumerate(['web', 'mobile', 'ai', 'ecommerce', 'enterprise', 'other'])}
        complexity_mapping = {c: i for i, c in enumerate(['simple', 'medium', 'complex', 'very-complex'])}
        timeline_mapping = {t: i for i, t in enumerate(['flexible', 'standard', 'urgent', 'asap'])}
        team_mapping = {t: i for i, t in enumerate(['solo', 'small', 'medium', 'large'])}
        
        features = pd.DataFrame()
        features['project_type'] = df['project_type'].map(type_mapping)
        features['complexity'] = df['complexity'].map(complexity_mapping)
        features['timeline'] = df['timeline'].map(timeline_mapping)
        features['team_size'] = df['team_size'].map(team_mapping)
        features['description_length'] = df['description_length']
        features['tech_terms_count'] = df['tech_terms_count']
        
        return features
    
    def _train_fallback_model(self):
        """Simple fallback model"""
        from sklearn.linear_model import LinearRegression
        sample_data = self._generate_training_data()
        df = pd.DataFrame(sample_data)
        X = self._engineer_features(df)
        y = df['price']
        
        model = LinearRegression()
        model.fit(X, y)
        return model
    
    def calculate_price(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate project price using AI model and OpenAI enhancement"""
        try:
            # Extract basic features
            features = self._extract_features(project_data)
            
            # Get base prediction from ML model
            base_prediction = self.model.predict([features])[0]
            
            # Enhance with OpenAI analysis for complex projects
            if project_data.get('complexity') in ['complex', 'very-complex']:
                enhanced_analysis = self._openai_enhancement(project_data, base_prediction)
                final_price = enhanced_analysis.get('enhanced_price', base_prediction)
                confidence = enhanced_analysis.get('confidence', 0.9)
                breakdown = enhanced_analysis.get('breakdown', {})
            else:
                final_price = base_prediction
                confidence = 0.85
                breakdown = self._generate_price_breakdown(project_data, final_price)
            
            # Apply South Africa market adjustment
            zar_price = final_price * 1.15  # Market adjustment factor
            zar_price = max(zar_price, 5000)  # Minimum project price
            
            # Round to nearest 100
            final_price_zar = round(zar_price / 100) * 100
            
            return {
                'base_price_usd': round(final_price / 18.5, 2),
                'final_price_zar': final_price_zar,
                'confidence_score': confidence,
                'price_breakdown': breakdown,
                'currency': 'ZAR',
                'market': 'South Africa'
            }
            
        except Exception as e:
            logger.error(f"Price calculation error: {e}")
            return self._fallback_calculation(project_data)
    
    def _extract_features(self, project_data: Dict[str, Any]) -> list:
        """Extract features for the model"""
        description = project_data.get('description', '')
        project_type = project_data.get('project_type', 'other')
        complexity = project_data.get('complexity', 'medium')
        timeline = project_data.get('timeline', 'standard')
        team_size = project_data.get('team_size', 'small')
        
        # Map to numerical values
        type_mapping = {'web': 0, 'mobile': 1, 'ai': 2, 'ecommerce': 3, 'enterprise': 4, 'other': 5}
        complexity_mapping = {'simple': 0, 'medium': 1, 'complex': 2, 'very-complex': 3}
        timeline_mapping = {'flexible': 0, 'standard': 1, 'urgent': 2, 'asap': 3}
        team_mapping = {'solo': 0, 'small': 1, 'medium': 2, 'large': 3}
        
        features = [
            type_mapping.get(project_type, 5),
            complexity_mapping.get(complexity, 1),
            timeline_mapping.get(timeline, 1),
            team_mapping.get(team_size, 1),
            len(description),
            self._count_tech_terms(description)
        ]
        
        return features
    
    def _count_tech_terms(self, description: str) -> int:
        """Count technology-related terms in description"""
        tech_terms = [
            'api', 'database', 'cloud', 'mobile', 'web', 'ai', 'ml', 'blockchain',
            'react', 'angular', 'vue', 'node', 'python', 'java', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'server', 'client', 'frontend', 'backend', 'fullstack'
        ]
        description_lower = description.lower()
        return sum(1 for term in tech_terms if term in description_lower)
    
    def _openai_enhancement(self, project_data: Dict[str, Any], base_price: float) -> Dict[str, Any]:
        """Use OpenAI to enhance pricing for complex projects"""
        try:
            prompt = f"""
            Analyze this software project and provide pricing recommendations:
            
            Project Type: {project_data.get('project_type')}
            Complexity: {project_data.get('complexity')}
            Timeline: {project_data.get('timeline')}
            Team Size: {project_data.get('team_size')}
            Description: {project_data.get('description', '')[:1000]}
            
            Base Price Estimate: R {base_price:,.2f}
            
            Consider:
            - South African market rates
            - Project complexity factors
            - Required technologies
            - Timeline constraints
            - Team size requirements
            
            Provide:
            1. Enhanced price recommendation in ZAR
            2. Confidence score (0-1)
            3. Detailed price breakdown
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are a expert software project pricing analyst specializing in the South African market."},
                         {"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            # Parse response (this would be more sophisticated in production)
            analysis = response.choices[0].message.content
            
            return {
                'enhanced_price': base_price * 1.1,  # Simplified for example
                'confidence': 0.92,
                'breakdown': self._generate_detailed_breakdown(project_data, base_price),
                'analysis': analysis[:500]  # Truncate for response
            }
            
        except Exception as e:
            logger.warning(f"OpenAI enhancement failed: {e}")
            return {
                'enhanced_price': base_price,
                'confidence': 0.8,
                'breakdown': self._generate_price_breakdown(project_data, base_price)
            }
    
    def _generate_price_breakdown(self, project_data: Dict[str, Any], total_price: float) -> Dict[str, float]:
        """Generate detailed price breakdown"""
        breakdown = {
            'development': total_price * 0.55,
            'project_management': total_price * 0.15,
            'quality_assurance': total_price * 0.12,
            'deployment': total_price * 0.08,
            'support_maintenance': total_price * 0.06,
            'security_implementation': total_price * 0.04
        }
        return breakdown
    
    def _generate_detailed_breakdown(self, project_data: Dict[str, Any], total_price: float) -> Dict[str, float]:
        """Generate more detailed breakdown for complex projects"""
        complexity = project_data.get('complexity', 'medium')
        
        if complexity == 'very-complex':
            breakdown = {
                'requirements_analysis': total_price * 0.08,
                'system_design': total_price * 0.07,
                'backend_development': total_price * 0.25,
                'frontend_development': total_price * 0.15,
                'database_design': total_price * 0.06,
                'api_development': total_price * 0.08,
                'testing_qa': total_price * 0.10,
                'security_implementation': total_price * 0.06,
                'deployment': total_price * 0.05,
                'documentation': total_price * 0.04,
                'training': total_price * 0.03,
                'support_maintenance': total_price * 0.03
            }
        else:
            breakdown = self._generate_price_breakdown(project_data, total_price)
        
        return breakdown
    
    def _fallback_calculation(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback pricing calculation"""
        base_prices = {
            'web': 85000, 'mobile': 135000, 'ai': 255000, 
            'ecommerce': 170000, 'enterprise': 340000, 'other': 119000
        }
        
        complexity_mult = {'simple': 0.7, 'medium': 1.0, 'complex': 1.8, 'very-complex': 2.5}
        timeline_mult = {'flexible': 0.9, 'standard': 1.0, 'urgent': 1.4, 'asap': 2.0}
        team_mult = {'solo': 0.8, 'small': 1.0, 'medium': 1.5, 'large': 2.2}
        
        base_price = base_prices.get(project_data.get('project_type', 'other'), 119000)
        price = base_price * complexity_mult.get(project_data.get('complexity', 'medium'), 1.0)
        price *= timeline_mult.get(project_data.get('timeline', 'standard'), 1.0)
        price *= team_mult.get(project_data.get('team_size', 'small'), 1.0)
        
        # Apply SA market adjustment
        price *= 1.15
        
        return {
            'base_price_usd': round(price / 18.5, 2),
            'final_price_zar': round(price / 100) * 100,
            'confidence_score': 0.7,
            'price_breakdown': self._generate_price_breakdown(project_data, price),
            'currency': 'ZAR',
            'market': 'South Africa'
        }
