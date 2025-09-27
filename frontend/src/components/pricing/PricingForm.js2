import React, { useState } from 'react';
import { Form, Button, Card, Row, Col, Alert, Spinner } from 'react-bootstrap';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';

const PricingForm = () => {
  const { isAuthenticated } = useAuth();
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

  if (!isAuthenticated) {
    return (
      <Alert variant="info">
        Please <a href="/login">login</a> or <a href="/register">register</a> to use the AI pricing engine.
      </Alert>
    );
  }

  return (
    <Card className="ai-pricing-form">
      <Card.Body>
        <h3 className="fw-bold mb-4">AI Project Pricing (ZAR)</h3>
        
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-4">
            <Form.Label className="fw-bold">Project Description</Form.Label>
            <Form.Control
              as="textarea"
              rows={5}
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Describe your project in detail..."
              required
            />
            <Form.Text className="text-muted">
              Be as detailed as possible for the most accurate pricing.
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
                  <option value="">Select project type</option>
                  <option value="web">Web Application</option>
                  <option value="mobile">Mobile App</option>
                  <option value="ai">AI/ML Solution</option>
                  <option value="ecommerce">E-commerce Platform</option>
                  <option value="enterprise">Enterprise Software</option>
                  <option value="other">Other</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="fw-bold">Complexity</Form.Label>
                <Form.Select
                  name="complexity"
                  value={formData.complexity}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select complexity</option>
                  <option value="simple">Simple</option>
                  <option value="medium">Medium</option>
                  <option value="complex">Complex</option>
                  <option value="very-complex">Very Complex</option>
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="fw-bold">Timeline</Form.Label>
                <Form.Select
                  name="timeline"
                  value={formData.timeline}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select timeline</option>
                  <option value="flexible">Flexible (3+ months)</option>
                  <option value="standard">Standard (1-3 months)</option>
                  <option value="urgent">Urgent (2-4 weeks)</option>
                  <option value="asap">ASAP (1-2 weeks)</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="fw-bold">Team Size</Form.Label>
                <Form.Select
                  name="team_size"
                  value={formData.team_size}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select team size</option>
                  <option value="solo">Solo Developer</option>
                  <option value="small">Small Team (2-3)</option>
                  <option value="medium">Medium Team (4-6)</option>
                  <option value="large">Large Team (7+)</option>
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
            className="w-100"
          >
            {loading ? (
              <>
                <Spinner animation="border" size="sm" className="me-2" />
                Analyzing...
              </>
            ) : (
              <>
                <i className="fas fa-calculator me-2"></i>
                Calculate Price (ZAR)
              </>
            )}
          </Button>
        </Form>

        {result && (
          <div className="mt-4 p-4 bg-light rounded fade-in">
            <Row className="align-items-center mb-4">
              <Col md={8}>
                <h4 className="fw-bold mb-1">Estimated Project Cost</h4>
                <p className="mb-0">Based on your description and selections</p>
              </Col>
              <Col md={4} className="text-end">
                <h2 className="zar-price">
                  {result.pricing.final_price_zar.toLocaleString('en-ZA')}
                </h2>
                <Button variant="accent" className="mt-2">
                  Add to Cart
                </Button>
              </Col>
            </Row>

            <div>
              <h5>AI Analysis Breakdown</h5>
              
              <div className="ai-helper">
                <i className="fas fa-brain"></i>
                <div>
                  <h6 className="mb-1">Project Analyzer</h6>
                  <p className="mb-0 small">
                    {result.ai_analysis.project_analyzer}
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
                <i className="fas fa-chart-line"></i>
                <div>
                  <h6 className="mb-1">Pricing Engine</h6>
                  <p className="mb-0 small">
                    {result.ai_analysis.pricing_engine}
                  </p>
                </div>
              </div>

              <div className="ai-helper">
                <i className="fas fa-bullhorn"></i>
                <div>
                  <h6 className="mb-1">Marketing Agent</h6>
                  <p className="mb-0 small">
                    {result.ai_analysis.marketing_agent}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </Card.Body>
    </Card>
  );
};

export default PricingForm;
