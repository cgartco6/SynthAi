# WhatsApp Integration Guide

## Overview

SynthAI integrates WhatsApp Business API via Twilio to provide instant customer support and AI-powered assistance.

## Features

- **Floating WhatsApp Button**: Always-visible button on the website
- **AI-Powered Responses**: Robyn chatbot handles common inquiries
- **24/7 Availability**: Automated responses outside business hours
- **Lead Generation**: Capture potential customers via WhatsApp
- **Human Handoff**: Escalate complex queries to human agents

## Setup Instructions

### 1. Twilio Account Setup

1. Create a Twilio account at https://twilio.com
2. Verify your phone number for WhatsApp
3. Get your Account SID and Auth Token
4. Set up WhatsApp sandbox or apply for business API

### 2. Environment Configuration

Add these variables to your `.env` file:

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
