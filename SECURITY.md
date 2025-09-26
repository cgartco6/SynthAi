# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of SynthAI seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not** disclose the vulnerability publicly
2. Email our security team at security@synthai.co.za
3. Include detailed information about the vulnerability
4. We will respond within 48 hours
5. We will work with you to understand and fix the issue

## Security Measures

### Data Encryption
- All data is encrypted at rest using AES-256
- TLS 1.3 for all data in transit
- End-to-end encryption for sensitive communications

### Authentication & Authorization
- Multi-factor authentication support
- JWT tokens with short expiration times
- Role-based access control

### Infrastructure Security
- Regular security patches and updates
- Network segmentation and firewalls
- DDoS protection and rate limiting

### Code Security
- Regular dependency vulnerability scanning
- Static code analysis
- Security code reviews

## Responsible Disclosure

We follow responsible disclosure practices. Security researchers who responsibly disclose vulnerabilities will be acknowledged in our release notes.
