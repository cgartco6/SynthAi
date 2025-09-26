import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import { AuthProvider } from './contexts/AuthContext';
import { CartProvider } from './contexts/CartContext';
import { ChatbotProvider } from './contexts/ChatbotContext';

// Components
import Navigation from './components/layout/Navigation';
import Footer from './components/layout/Footer';
import Chatbot from './components/chatbot/Chatbot';

// Pages
import Home from './pages/Home';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Pricing from './pages/Pricing';
import Projects from './pages/Projects';
import Marketing from './pages/Marketing';
import Cart from './pages/Cart';
import Dashboard from './pages/Dashboard';

// Styles
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <ChatbotProvider>
          <Router>
            <div className="App">
              <Navigation />
              <main className="main-content">
                <Container fluid>
                  <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/pricing" element={<Pricing />} />
                    <Route path="/projects" element={<Projects />} />
                    <Route path="/marketing" element={<Marketing />} />
                    <Route path="/cart" element={<Cart />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                  </Routes>
                </Container>
              </main>
              <Footer />
              <Chatbot />
            </div>
          </Router>
        </ChatbotProvider>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;
