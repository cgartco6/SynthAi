import os
import logging
import openai
from typing import Dict, Any
import re

logger = logging.getLogger(__name__)

class ChatbotAI:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.conversation_context = {}
    
    def process_whatsapp_message(self, message: str, phone_number: str) -> str:
        """
        Process WhatsApp messages and generate AI responses
        """
        try:
            # Get or create conversation context
            if phone_number not in self.conversation_context:
                self.conversation_context[phone_number] = {
                    'history': [],
                    'user_info': {},
                    'conversation_stage': 'greeting'
                }
            
            context = self.conversation_context[phone_number]
            
            # Classify message intent
            intent = self._classify_intent(message)
            
            # Generate response based on intent
            if intent == 'pricing_inquiry':
                response = self._handle_pricing_inquiry(message, context)
            elif intent == 'project_help':
                response = self._handle_project_help(message, context)
            elif intent == 'technical_support':
                response = self._handle_technical_support(message, context)
            elif intent == 'marketing_info':
                response = self._handle_marketing_info(message, context)
            elif intent == 'greeting':
                response = self._handle_greeting(message, context)
            else:
                response = self._handle_general_inquiry(message, context)
            
            # Update conversation history
            context['history'].append({
                'user_message': message,
                'bot_response': response,
                'intent': intent
            })
            
            # Keep only last 10 messages in history
            if len(context['history']) > 10:
                context['history'] = context['history'][-10:]
            
            return response
            
        except Exception as e:
            logger.error(f"Chatbot processing error: {e}")
            return self._get_fallback_response()
    
    def _classify_intent(self, message: str) -> str:
        """
        Classify the intent of the user message
        """
        message_lower = message.lower()
        
        # Intent classification logic
        pricing_keywords = ['price', 'cost', 'how much', 'pricing', 'quote', 'budget']
        project_keywords = ['project', 'develop', 'build', 'create', 'website', 'app']
        technical_keywords = ['help', 'support', 'problem', 'issue', 'error', 'technical']
        marketing_keywords = ['marketing', 'social media', 'promote', 'advertise']
        greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        
        if any(keyword in message_lower for keyword in pricing_keywords):
            return 'pricing_inquiry'
        elif any(keyword in message_lower for keyword in project_keywords):
            return 'project_help'
        elif any(keyword in message_lower for keyword in technical_keywords):
            return 'technical_support'
        elif any(keyword in message_lower for keyword in marketing_keywords):
            return 'marketing_info'
        elif any(keyword in message_lower for keyword in greeting_keywords):
            return 'greeting'
        else:
            return 'general_inquiry'
    
    def _handle_greeting(self, message: str, context: Dict[str, Any]) -> str:
        """Handle greeting messages"""
        responses = [
            "Hello! 👋 I'm Robyn from SynthAI. How can I help you today?",
            "Hi there! 🤖 I'm Robyn, your AI assistant from SynthAI. What can I do for you?",
            "Welcome to SynthAI! I'm Robyn, ready to help with your project needs. How can I assist you?"
        ]
        
        # Update conversation stage
        context['conversation_stage'] = 'active'
        
        return responses[hash(message) % len(responses)]
    
    def _handle_pricing_inquiry(self, message: str, context: Dict[str, Any]) -> str:
        """Handle pricing-related inquiries"""
        prompt = f"""
        User is asking about pricing: "{message}"
        
        Provide a helpful response about SynthAI's AI-powered pricing:
        - We use AI to provide accurate project estimates in ZAR
        - Pricing depends on project complexity, timeline, and requirements
        - We offer free project analysis
        - Direct them to our website for detailed pricing
        
        Keep it friendly and encouraging. Response should be under 300 characters.
        """
        
        try:
            response = self._get_openai_response(prompt)
            return response + "\n\n💡 Want a detailed quote? Visit: https://synthai.co.za/pricing"
        except Exception as e:
            return "We provide AI-powered project pricing in ZAR! Our system analyzes your requirements for accurate estimates. Visit https://synthai.co.za/pricing for a free quote! 💰"
    
    def _handle_project_help(self, message: str, context: Dict[str, Any]) -> str:
        """Handle project-related inquiries"""
        prompt = f"""
        User needs help with a project: "{message}"
        
        As SynthAI's assistant, explain how we can help:
        - AI-powered project planning and pricing
        - Full-stack development services
        - South Africa market expertise
        - Military-grade security
        
        Keep it professional yet friendly. Under 300 characters.
        """
        
        try:
            response = self._get_openai_response(prompt)
            return response + "\n\n🚀 Let's discuss your project! Visit: https://synthai.co.za"
        except Exception as e:
            return "We specialize in AI-powered project development! From web apps to enterprise solutions, we've got you covered. Let's discuss your project at https://synthai.co.za! 🛠️"
    
    def _handle_technical_support(self, message: str, context: Dict[str, Any]) -> str:
        """Handle technical support inquiries"""
        prompt = f"""
        User needs technical support: "{message}"
        
        Respond as SynthAI's support assistant:
        - Offer help with technical issues
        - Mention our expertise
        - Provide support options
        - Be helpful and reassuring
        
        Keep it under 250 characters.
        """
        
        try:
            response = self._get_openai_response(prompt)
            return response + "\n\n🔧 Need immediate help? Email: support@synthai.co.za"
        except Exception as e:
            return "I'm here to help with technical questions! For detailed support, our team is available via email at support@synthai.co.za. We'll get you sorted! ⚡"
    
    def _handle_marketing_info(self, message: str, context: Dict[str, Any]) -> str:
        """Handle marketing-related inquiries"""
        prompt = f"""
        User is asking about marketing services: "{message}"
        
        Explain SynthAI's marketing services:
        - Social media marketing (TikTok, Facebook, Instagram, etc.)
        - AI-powered campaign optimization
        - South Africa market targeting
        - Performance analytics
        
        Keep it engaging. Under 300 characters.
        """
        
        try:
            response = self._get_openai_response(prompt)
            return response + "\n\n📱 Boost your presence! See packages: https://synthai.co.za/marketing"
        except Exception as e:
            return "We offer AI-powered social media marketing across all platforms! TikTok, Facebook, Instagram, and more. Get your brand noticed! Check our packages at https://synthai.co.za/marketing 🎯"
    
    def _handle_general_inquiry(self, message: str, context: Dict[str, Any]) -> str:
        """Handle general inquiries using OpenAI"""
        prompt = f"""
        User message: "{message}"
        
        You are Robyn, an AI assistant for SynthAI - a South African AI-powered project 
        development and pricing platform. Respond helpfully and professionally.
        
        Key points about SynthAI:
        - AI-powered project pricing and development
        - Social media marketing services
        - Military-grade security
        - South Africa focused (ZAR pricing)
        - WhatsApp: +27 72 142 3215
        - Website: https://synthai.co.za
        
        Keep response under 300 characters. Be friendly and helpful.
        """
        
        try:
            response = self._get_openai_response(prompt)
            return response
        except Exception as e:
            return self._get_fallback_response()
    
    def _get_openai_response(self, prompt: str) -> str:
        """Get response from OpenAI GPT"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Robyn, a helpful AI assistant for SynthAI."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise e
    
    def _get_fallback_response(self) -> str:
        """Fallback response when AI fails"""
        fallback_responses = [
            "I'd be happy to help! Could you provide more details about what you're looking for?",
            "Thanks for your message! Our team can assist you with that. Visit https://synthai.co.za for more info.",
            "I'm here to help! For detailed assistance, you can reach us at info@synthai.co.za or +27 72 142 3215."
        ]
        
        return fallback_responses[hash(str(len(fallback_responses))) % len(fallback_responses)]
