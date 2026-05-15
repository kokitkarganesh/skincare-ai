import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

const RoutineCard = ({ title, icon, steps, treatments, color }) => {
  const [expandedSteps, setExpandedSteps] = useState([]);

  const toggleStep = (index) => {
    setExpandedSteps(prev => 
      prev.includes(index) 
        ? prev.filter(i => i !== index)
        : [...prev, index]
    );
  };

  return (
    <div className={`routine-card ${color}`}>
      <div className="routine-header">
        {icon}
        <h3>{title}</h3>
      </div>

      {steps && (
        <div className="routine-steps">
          {steps.map((step, index) => (
            <div key={index} className="routine-step">
              <div 
                className="step-header"
                onClick={() => toggleStep(index)}
              >
                <div className="step-number">{index + 1}</div>
                <div className="step-title">
                  <h4>{step.step}</h4>
                  <p className="step-why">{step.why}</p>
                </div>
                {expandedSteps.includes(index) ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
              </div>

              {expandedSteps.includes(index) && (
                <div className="step-details">
                  <div className="option">
                    <span className="option-label">🏪 Commercial:</span>
                    <span className="option-text">{step.commercial}</span>
                  </div>
                  <div className="option">
                    <span className="option-label">🌿 Natural:</span>
                    <span className="option-text">{step.natural}</span>
                  </div>
                  <div className="option">
                    <span className="option-label">🏡 Home Remedy:</span>
                    <span className="option-text">{step.home_remedy}</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {treatments && (
        <div className="treatments-list">
          {treatments.map((treatment, index) => (
            <div key={index} className="treatment-item">
              {treatment}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RoutineCard;