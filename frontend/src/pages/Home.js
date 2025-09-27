import React from 'react';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import WhatsAppFloat from '../components/layout/WhatsAppFloat';

const Home = () => {
  const phoneNumber = "27721423215";
  const message = "Hi%20SynthAI%2C%20I%20would%20like%20to%20get%20more%20information%20about%20your%20services.";
  const whatsappUrl = `https://wa.me/${phoneNumber}?text=${message}`;

  return (
    <>
      {/* Hero Section */}
      <section className="hero-section">
        <Container>
          <Row>
            <Col lg={8} className="mx-auto text-center">
              <h1 className="display-4 fw-bold mb-4">AI-Powered Project Solutions</h1>
              <p className="lead mb-4">
                Our synthetic intelligence team analyzes your project requirements and provides 
                instant pricing in ZAR with military-grade security.
              </p>
              <div className="d-flex gap-3 justify-content-center flex-wrap">
                <Link to="/pricing" className="btn btn-light btn-lg">
                  Get Your Project Priced
                </Link>
                <a 
                  href={whatsappUrl} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="btn btn-outline-light btn-lg"
                >
                  <i className="fab fa-whatsapp me-2"></i>
                  Chat on WhatsApp
                </a>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      {/* WhatsApp Section */}
      <section className="whatsapp-section">
        <Container>
          <Row>
            <Col lg={8} className="mx-auto text-center">
              <Card className="whatsapp-card">
                <i className="fab fa-whatsapp whatsapp-icon"></i>
                <h3 className="mb-3">Instant Support via WhatsApp</h3>
                <p className="mb-4">
                  Get immediate assistance from our AI experts. We're available 24/7 to help 
                  with your project inquiries, pricing questions, and technical support.
                </p>
                <a 
                  href={whatsappUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="whatsapp-btn"
                >
                  <i className="fab fa-whatsapp"></i>
                  Start Chat Now
                </a>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Rest of the home page content... */}

      <WhatsAppFloat />
    </>
  );
};

export default Home;
