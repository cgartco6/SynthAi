# Update the pricing inquiry handler
def _handle_pricing_inquiry(self, message: str, context: Dict[str, Any]) -> str:
    """Handle pricing-related inquiries with affordable messaging"""
    prompt = f"""
    User is asking about pricing: "{message}"
    
    Provide a helpful response about SynthAI's NEW AFFORDABLE AI-powered pricing:
    - We've reduced prices by 60% for South African businesses
    - Simple websites start from R5,000
    - E-commerce stores from R15,000
    - Mobile apps from R20,000
    - We offer free project analysis
    - Direct them to our website for instant quotes
    
    Keep it friendly and encouraging. Highlight the affordability.
    Response should be under 300 characters.
    """
    
    try:
        response = self._get_openai_response(prompt)
        return response + "\n\n💡 Get your affordable quote now: https://synthai.co.za/pricing"
    except Exception as e:
        return "Great news! 🎉 We've reduced our prices by 60%! Simple websites from R5,000, e-commerce from R15,000. Get your instant affordable quote at https://synthai.co.za/pricing 💰"
