import React, { useState } from 'react';
import { Form, Button, Card, Row, Col, Alert, Spinner, Badge } from 'react-bootstrap';
import { useAuth } from '../../contexts/AuthContext';
import { useCart } from '../../contexts/CartContext';
import axios from 'axios';

const PricingForm = () => {
  const { isAuthenticated } = useAuth();
  const { addToCart } = useCart();
  const [formData, setFormData] = useState({
    description: '',
    project_type: '',
    complexity: '',
    timeline: '',
    team_size: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post('/api/pricing/analyze', formData);
      setResult(response.data);
    } catch (error) {
      setError(error.response?.data?.error || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = () => {
    if (result) {
      addToCart(
        `${formData.project_type} Project - ${formData.complexity} complexity`,
        result.pricing.final_price_zar,
        'project'
      );
    }
  };

  // Affordable pricing examples for quick reference
  const affordableExamples = [
    { type: 'Simple Website', price: 'R 5,000 - R 15,000', desc: 'Basic landing page or portfolio' },
    { type: 'E-commerce Store', price: 'R 15,000 - R 40,000', desc: 'Online store with payment processing' },
    { type: 'Mobile App', price: 'R 20,000 - R 50,000', desc: 'Cross-platform mobile application' },
    { type: 'Business Software', price: 'R 25,000 - R 80,000', desc: 'Custom business management system' }
  ];

  if (!isAuthenticated) {
    return (
      <Alert variant="info">
        <strong>Affordable AI Pricing!</strong> Please <a href="/login">login</a> or <a href="/register">register</a> 
        to get your personalized project quote. Our prices are now 60% more affordable for South African businesses.
      </Alert>
    );
  }

  return (
    <Card className="ai-pricing-form">
      <Card.Body>
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h3 className="fw-bold mb-0">AI Project Pricing (ZAR)</h3>
          <Badge bg="success" className="fs-6">
            <i className="fas fa-tag me-1"></i>
            60% More Affordable
          </Badge>
        </div>
        
        <p className="text-muted mb-4">
          Get instant AI-powered pricing tailored for South African businesses. 
          Our new affordable rates make quality development accessible to everyone.
        </p>

        {/* Affordable Pricing Examples */}
        <Row className="mb-4">
          <Col>
            <h5 className="fw-bold mb-3">💡 Affordable Project Examples</h5>
            <div className="row g-3">
              {affordableExamples.map((example, index) => (
                <div key={index} className="col-md-6">
                  <Card className="h-100 border-0 bg-light">
                    <Card.Body className="p-3">
                      <h6 className="fw-bold text-primary mb-1">{example.type}</h6>
                      <div className="zar-price-small mb-1">{example.price}</div>
                      <small className="text-muted">{example.desc}</small>
                    </Card.Body>
                  </Card>
                </div>
              ))}
            </div>
          </Col>
        </Row>

        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-4">
            <Form.Label className="fw-bold">
              Project Description <small className="text-muted">(What do you want to build?)</small>
            </Form.Label>
            <Form.Control
              as="textarea"
              rows={4}
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Describe your project in simple terms... What problem are you solving? What features do you need?"
              required
            />
            <Form.Text className="text-muted">
              Be specific about your goals. The more details, the more accurate our AI pricing will be.
            </Form.Text>
          </Form.Group>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="fw-bold">Project Type</Form.Label>
                <Form.Select
                  name="project_type"
                  value={formData.project_type}
                  onChange={handleChange}
                  required
                >
                  <option value="">What are you building?</option>
                  <option value="web">Website / Web Application</option>
                  <option value="mobile">Mobile App</option>
                  <option value="ecommerce">E-commerce Store</option>
                  <option value="ai">AI / Machine Learning</option>
                  <option value="enterprise">Business Software</option>
                  <option value="other">Other Project</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="fw-bold">
                  Complexity <small className="text-muted">(How complex is your project?)</small>
                </Form.Label>
                <Form.Select
                  name="complexity"
                  value={formData.complexity}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select complexity level</option>
                  <option value="simple">Simple (Basic features, standard design)</option>
                  <option value="medium">Medium (Multiple features, custom design)</option>
                  <option value="complex">Complex (Advanced features, complex logic)</option>
                  <option value="very-complex">Very Complex (Cutting-edge technology)</option>
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="fw-bold">
                  Timeline <small className="text-muted">(When do you need it?)</small>
                </Form.Label>
                <Form.Select
                  name="timeline"
                  value={formData.timeline}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select your timeline</option>
                  <option value="flexible">Flexible (3+ months) - Most Affordable</option>
                  <option value="standard">Standard (1-3 months) - Balanced</option>
                  <option value="urgent">Urgent (2-4 weeks) - Faster Delivery</option>
                  <option value="asap">ASAP (1-2 weeks) - Premium Rush</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="fw-bold">
                  Team Size <small className="text-muted">(How many developers?)</small>
                </Form.Label>
                <Form.Select
                  name="team_size"
                  value={formData.team_size}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select team size</option>
                  <option value="solo">Solo Developer - Most Affordable</option>
                  <option value="small">Small Team (2-3) - Recommended</option>
                  <option value="medium">Medium Team (4-6) - Comprehensive</option>
                  <option value="large">Large Team (7+) - Enterprise</option>
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>

          {error && <Alert variant="danger">{error}</Alert>}

          <Button 
            type="submit" 
            variant="primary" 
            size="lg" 
            disabled={loading}
            className="w-100 py-3"
          >
            {loading ? (
              <>
                <Spinner animation="border" size="sm" className="me-2" />
                AI is calculating your affordable price...
              </>
            ) : (
              <>
                <i className="fas fa-calculator me-2"></i>
                Get Your Affordable Price Quote
              </>
            )}
          </Button>
        </Form>

        {result && (
          <div className="mt-4 p-4 bg-light rounded fade-in">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h4 className="fw-bold mb-0 text-success">
                <i className="fas fa-badge-check me-2"></i>
                Your Affordable Quote
              </h4>
              <Badge bg="success" className="fs-6">
                AI Verified
              </Badge>
            </div>
            
            <Row className="align-items-center mb-4">
              <Col md={8}>
                <p className="mb-1">Perfect for {formData.complexity} {formData.project_type} projects</p>
                <small className="text-muted">
                  {formData.team_size} team • {formData.timeline} timeline
                </small>
              </Col>
              <Col md={4} className="text-end">
                <h2 className="zar-price mb-2">
                  {result.pricing.final_price_zar.toLocaleString('en-ZA')}
                </h2>
                <div className="d-flex gap-2 justify-content-end">
                  <Button variant="outline-primary" size="sm">
                    <i className="fas fa-download me-1"></i>
                    Save Quote
                  </Button>
                  <Button variant="success" size="sm" onClick={handleAddToCart}>
                    <i className="fas fa-cart-plus me-1"></i>
                    Add to Cart
                  </Button>
                </div>
              </Col>
            </Row>

            {/* Affordable Price Breakdown */}
            <div className="mb-4">
              <h6 className="fw-bold mb-3">💰 Affordable Price Breakdown</h6>
              <Row>
                {Object.entries(result.pricing.price_breakdown).map(([key, value]) => (
                  <Col key={key} md={6} className="mb-2">
                    <div className="d-flex justify-content-between">
                      <span className="text-capitalize">{key.replace('_', ' ')}:</span>
                      <strong>R {value.toLocaleString('en-ZA')}</strong>
                    </div>
                  </Col>
                ))}
              </Row>
            </div>

            <div>
              <h6 className="fw-bold mb-3">🤖 AI Analysis</h6>
              
              <div className="ai-helper affordable">
                <i className="fas fa-piggy-bank text-success"></i>
                <div>
                  <h6 className="mb-1">Affordable Pricing Engine</h6>
                  <p className="mb-0 small">
                    Optimized for South African market • 60% more affordable • Best value guarantee
                  </p>
                </div>
              </div>

              <div className="ai-helper">
                <i className="fas fa-cogs"></i>
                <div>
                  <h6 className="mb-1">Tech Recommender</h6>
                  <p className="mb-0 small">
                    {result.ai_analysis.tech_recommender}
                  </p>
                </div>
              </div>

              <div className="ai-helper">
                <i className="fas fa-shield-alt"></i>
                <div>
                  <h6 className="mb-1">Security Audit</h6>
                  <p className="mb-0 small">
                    {result.ai_analysis.security_auditor}
                  </p>
                </div>
              </div>
            </div>

            {/* Call to Action */}
            <div className="mt-4 p-3 bg-white rounded border">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="fw-bold mb-1">Ready to start your project?</h6>
                  <small className="text-muted">Get started today with our affordable pricing</small>
                </div>
                <Button variant="primary" onClick={handleAddToCart}>
                  <i className="fas fa-rocket me-1"></i>
                  Start Project
                </Button>
              </div>
            </div>
          </div>
        )}
      </Card.Body>
    </Card>
  );
};

export default PricingForm;
