import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Stethoscope, MessageCircle, ArrowRight } from 'lucide-react';

const Hero = () => {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1 className="hero-title">
          AI-Powered Skincare Analysis
        </h1>
        <p className="hero-subtitle">
          Get personalized skincare recommendations, disease detection, and expert advice powered by advanced AI
        </p>

        <div className="features-grid">
          <Link to="/disease-detection" className="feature-card">
            <div className="feature-icon">
              <Stethoscope size={40} />
            </div>
            <h3>Disease Detection</h3>
            <p>Detect 10 skin diseases using AI ensemble models</p>
            <span className="feature-arrow">
              Get Started <ArrowRight size={16} />
            </span>
          </Link>

          <Link to="/skincare-analysis" className="feature-card">
            <div className="feature-icon">
              <Sparkles size={40} />
            </div>
            <h3>Skincare Analysis</h3>
            <p>Personalized routines with natural & commercial options based on your skin type</p>
            <span className="feature-arrow">
              Analyze Now <ArrowRight size={16} />
            </span>
          </Link>

          <Link to="/chatbot" className="feature-card">
            <div className="feature-icon">
              <MessageCircle size={40} />
            </div>
            <h3>AI Assistant</h3>
            <p>skincare advice with expert recommendations and home remedies</p>
            <span className="feature-arrow">
              Chat Now <ArrowRight size={16} />
            </span>
          </Link>
        </div>

        <div className="hero-stats">
          <div className="stat">
            <p>Disease Detection</p>
          </div>
          <div className="stat">
            <p>Skin Type Classification</p>
          </div>
          <div className="stat">
            <p>Free & Open Source</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;