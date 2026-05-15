import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sparkles, Stethoscope, MessageCircle, Home } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <Sparkles size={28} />
          <span>SkinCare AI</span>
        </Link>

        <ul className="navbar-menu">
          <li>
            <Link 
              to="/" 
              className={`navbar-link ${isActive('/') ? 'active' : ''}`}
            >
              <Home size={20} />
              Home
            </Link>
          </li>
          <li>
            <Link 
              to="/disease-detection" 
              className={`navbar-link ${isActive('/disease-detection') ? 'active' : ''}`}
            >
              <Stethoscope size={20} />
              Disease Detection
            </Link>
          </li>
          <li>
            <Link 
              to="/skincare-analysis" 
              className={`navbar-link ${isActive('/skincare-analysis') ? 'active' : ''}`}
            >
              <Sparkles size={20} />
              Skincare Analysis
            </Link>
          </li>
          <li>
            <Link 
              to="/chatbot" 
              className={`navbar-link ${isActive('/chatbot') ? 'active' : ''}`}
            >
              <MessageCircle size={20} />
              AI Assistant
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;