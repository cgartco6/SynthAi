import React from 'react';
import { Button, OverlayTrigger, Tooltip } from 'react-bootstrap';

const WhatsAppFloat = () => {
  const phoneNumber = "27721423215"; // South Africa format with country code
  const message = "Hi%20SynthAI%2C%20I%20would%20like%20to%20get%20more%20information%20about%20your%20services.";
  const whatsappUrl = `https://wa.me/${phoneNumber}?text=${message}`;

  return (
    <OverlayTrigger
      placement="left"
      overlay={<Tooltip>Chat with us on WhatsApp</Tooltip>}
    >
      <Button
        variant="success"
        size="lg"
        className="whatsapp-float"
        href={whatsappUrl}
        target="_blank"
        rel="noopener noreferrer"
      >
        <i className="fab fa-whatsapp"></i>
      </Button>
    </OverlayTrigger>
  );
};

export default WhatsAppFloat;
