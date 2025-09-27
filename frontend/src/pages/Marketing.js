import React from 'react';
import { Container, Row, Col, Card, Button, Badge } from 'react-bootstrap';
import { useCart } from '../contexts/CartContext';

const Marketing = () => {
  const { addToCart } = useCart();

  // Affordable marketing packages (reduced by 60%)
  const marketingPackages = [
    {
      id: 'tiktok',
      name: 'TikTok Campaigns',
      icon: 'fab fa-tiktok',
      price: 2000, // Reduced from 5,000
      duration: '30 days',
      description: 'Engaging short-form video content tailored for viral potential',
      features: ['5 viral videos', 'Hashtag strategy', 'Trend analysis', 'Performance analytics'],
      popular: true
    },
    {
      id: 'facebook',
      name: 'Facebook Marketing',
      icon: 'fab fa-facebook',
      price: 1800, // Reduced from 4,500
      duration: '30 days',
      description: 'Targeted ads and community building for maximum reach',
      features: ['Ad campaign management', 'Audience targeting', 'A/B testing', 'ROI tracking'],
      popular: false
    },
    {
      id: 'instagram',
      name: 'Instagram Strategy',
      icon: 'fab fa-instagram',
      price: 1700, // Reduced from 4,200
      duration: '30 days',
      description: 'Visual storytelling and influencer collaborations',
      features: ['Content creation', 'Influencer outreach', 'Story campaigns', 'Engagement analysis'],
      popular: false
    },
    {
      id: 'linkedin',
      name: 'LinkedIn Outreach',
      icon: 'fab fa-linkedin',
      price: 2400, // Reduced from 6,000
      duration: '30 days',
      description: 'Professional network building and B2B marketing',
      features: ['Company page optimization', 'Content marketing', 'Lead generation', 'Analytics'],
      popular: false
    },
    {
      id: 'twitter',
      name: 'Twitter Engagement',
      icon: 'fab fa-twitter',
      price: 1500, // Reduced from 3,800
      duration: '30 days',
      description: 'Real-time conversations and trend participation',
      features: ['Tweet strategy', 'Hashtag campaigns', 'Community management', 'Trend analysis'],
      popular: false
    },
    {
      id: 'email',
      name: 'Email Campaigns',
      icon: 'fas fa-envelope',
      price: 1000, // Reduced from 2,500
      duration: '30 days',
      description: 'Personalized communication and lead nurturing',
      features: ['Email design', 'Automation setup', 'List management', 'Performance tracking'],
      popular: false
    }
  ];

  const handleAddToCart = (package) => {
    addToCart(
      `${package.name} Marketing Package`,
      package.price,
      'marketing',
      { duration: package.duration }
    );
  };

  return (
    <div className="marketing-page">
      {/* Hero Section */}
      <section className="marketing-gradient text-white py-5">
        <Container>
          <Row>
            <Col lg={8} className="mx-auto text-center">
              <Badge bg="light" text="dark" className="mb-3 fs-6">
                🎯 60% More Affordable
              </Badge>
              <h1 className="display-5 fw-bold mb-3">AI-Powered Social Media Marketing</h1>
              <p className="lead mb-4">
                Now 60% more affordable! Get professional social media marketing 
                starting from just <strong>R 1,000/month</strong>. Perfect for South African businesses.
              </p>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Pricing Section */}
      <section className="py-5">
        <Container>
          <Row className="mb-5">
            <Col lg={8} className="mx-auto text-center">
              <h2 className="fw-bold mb-3">Affordable Marketing Packages</h2>
              <p className="text-muted">
                Choose the perfect package for your business. All packages include AI-powered optimization 
                and performance analytics.
              </p>
            </Col>
          </Row>

          <Row>
            {marketingPackages.map((pkg) => (
              <Col key={pkg.id} lg={4} md={6} className="mb-4">
                <Card className={`h-100 marketing-card ${pkg.popular ? 'popular' : ''}`}>
                  {pkg.popular && (
                    <div className="popular-badge">Most Popular</div>
                  )}
                  <Card.Body className="text-center p-4">
                    <i className={`${pkg.icon} fa-3x text-primary mb-3`}></i>
                    <h5 className="fw-bold">{pkg.name}</h5>
                    <p className="text-muted">{pkg.description}</p>
                    
                    <div className="marketing-price mb-3">
                      R {pkg.price.toLocaleString('en-ZA')}
                      <small className="text-muted">/{pkg.duration}</small>
                    </div>

                    <ul className="list-unstyled mb-4">
                      {pkg.features.map((feature, index) => (
                        <li key={index} className="mb-2">
                          <i className="fas fa-check text-success me-2"></i>
                          {feature}
                        </li>
                      ))}
                    </ul>

                    <Button 
                      variant={pkg.popular ? "primary" : "outline-primary"} 
                      className="w-100"
                      onClick={() => handleAddToCart(pkg)}
                    >
                      <i className="fas fa-cart-plus me-2"></i>
                      Add to Cart
                    </Button>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>

          {/* Bundle Deal */}
          <Row className="mt-5">
            <Col lg={8} className="mx-auto">
              <Card className="border-success">
                <Card.Body className="text-center p-5">
                  <Badge bg="success" className="mb-3">Bundle & Save</Badge>
                  <h4 className="fw-bold mb-3">Complete Marketing Suite</h4>
                  <p className="text-muted mb-4">
                    Get all 6 marketing platforms for one affordable price
                  </p>
                  <div className="d-flex justify-content-center align-items-center mb-4">
                    <div className="me-4">
                      <s className="text-muted">R 10,400</s>
                      <div className="fs-2 fw-bold text-success">
                        R 7,280<span className="fs-6">/month</span>
                      </div>
                      <small className="text-muted">Save 30% with bundle</small>
                    </div>
                    <Button variant="success" size="lg">
                      <i className="fas fa-gem me-2"></i>
                      Get Bundle Deal
                    </Button>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>
    </div>
  );
};

export default Marketing;
