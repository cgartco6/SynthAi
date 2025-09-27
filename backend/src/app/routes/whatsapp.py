from flask import Blueprint, request, jsonify
from twilio.rest import Client
import os
import logging
from ..models import db, User, Project, AuditLog
from ..ai_team.chatbot import ChatbotAI

whatsapp_bp = Blueprint('whatsapp', __name__)
logger = logging.getLogger(__name__)

# Initialize Twilio client
twilio_client = Client(
    os.environ.get('TWILIO_ACCOUNT_SID'),
    os.environ.get('TWILIO_AUTH_TOKEN')
)

chatbot_ai = ChatbotAI()

@whatsapp_bp.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """
    Webhook for handling WhatsApp messages via Twilio
    """
    try:
        # Get incoming message data
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        message_sid = request.values.get('MessageSid', '')
        
        logger.info(f"Received WhatsApp message from {from_number}: {incoming_msg}")
        
        # Process message with AI chatbot
        response = chatbot_ai.process_whatsapp_message(incoming_msg, from_number)
        
        # Send response back via WhatsApp
        if response:
            send_whatsapp_message(from_number, response)
        
        # Log the interaction
        log_audit_event(
            user_id=None,
            action='WHATSAPP_MESSAGE_RECEIVED',
            resource_type='WHATSAPP',
            resource_id=message_sid,
            details={
                'from_number': from_number,
                'message': incoming_msg,
                'response': response
            }
        )
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {e}")
        return jsonify({'error': 'Webhook processing failed'}), 500

def send_whatsapp_message(to_number, message):
    """
    Send WhatsApp message using Twilio
    """
    try:
        from_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_NUMBER')
        
        message = twilio_client.messages.create(
            body=message,
            from_=f'whatsapp:{from_whatsapp_number}',
            to=f'whatsapp:{to_number}'
        )
        
        logger.info(f"WhatsApp message sent to {to_number}: {message.sid}")
        return message.sid
        
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message: {e}")
        return None

@whatsapp_bp.route('/send-message', methods=['POST'])
def send_whatsapp_message_api():
    """
    API endpoint to send WhatsApp messages (for admin/automated use)
    """
    try:
        data = request.get_json()
        to_number = data.get('to_number')
        message = data.get('message')
        
        if not to_number or not message:
            return jsonify({'error': 'to_number and message are required'}), 400
        
        message_sid = send_whatsapp_message(to_number, message)
        
        if message_sid:
            return jsonify({
                'status': 'success',
                'message_sid': message_sid
            })
        else:
            return jsonify({'error': 'Failed to send message'}), 500
            
    except Exception as e:
        logger.error(f"WhatsApp API error: {e}")
        return jsonify({'error': 'Message sending failed'}), 500

def log_audit_event(user_id, action, resource_type, resource_id, details):
    """
    Log security events for audit trail
    """
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        details=details
    )
    db.session.add(audit_log)
    db.session.commit()
