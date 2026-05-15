import React from 'react';
import { AlertTriangle, CheckCircle, AlertCircle, TrendingUp } from 'lucide-react';

const DiseaseResults = ({ results, onReset }) => {
  const { status, top_prediction, all_predictions, warning, message } = results;

  const isLowConfidence = status === 'low_confidence' || warning;
  const topDisease = top_prediction.disease;
  const topConfidence = top_prediction.confidence;

  // Disease information database
  const diseaseInfo = {
  'Eczema': {
    description: 'A condition causing dry, itchy, inflamed skin.',
    severity: 'mild-moderate',
    action: 'Use moisturizers and consult dermatologist if severe.',
    treatmentOptions: 'Moisturizers, steroids, lifestyle changes'
  },

  'Warts Molluscum and other Viral Infections': {
    description: 'Viral skin infections causing bumps or lesions.',
    severity: 'mild',
    action: 'May resolve on their own, consult if persistent.',
    treatmentOptions: 'Cryotherapy, topical treatments'
  },

  'Melanoma': {
    description: 'Serious form of skin cancer.',
    severity: 'serious',
    action: 'URGENT: See dermatologist immediately.',
    treatmentOptions: 'Surgery, immunotherapy'
  },

  'Atopic Dermatitis': {
    description: 'Chronic inflammatory skin condition.',
    severity: 'mild-moderate',
    action: 'Manage with skincare and medical guidance.',
    treatmentOptions: 'Moisturizers, steroids'
  },

  'Basal Cell Carcinoma (BCC)': {
    description: 'Common skin cancer, slow growing.',
    severity: 'serious',
    action: 'Consult dermatologist for treatment.',
    treatmentOptions: 'Surgery, topical therapy'
  },

  'Melanocytic Nevi (NV)': {
    description: 'Common mole, usually benign.',
    severity: 'benign',
    action: 'Monitor for changes.',
    treatmentOptions: 'Observation or removal'
  },

  'Benign Keratosis-like Lesions (BKL)': {
    description: 'Non-cancerous skin growth.',
    severity: 'benign',
    action: 'Usually harmless.',
    treatmentOptions: 'Optional removal'
  },

  'Psoriasis Lichen Planus and related diseases': {
    description: 'Autoimmune skin condition causing scaling.',
    severity: 'moderate',
    action: 'Consult dermatologist.',
    treatmentOptions: 'Topical therapy, immunotherapy'
  },

  'Seborrheic Keratoses and other Benign Tumors': {
    description: 'Benign skin growths.',
    severity: 'benign',
    action: 'No treatment needed unless cosmetic.',
    treatmentOptions: 'Removal if needed'
  },

  'Tinea Ringworm Candidiasis and other Fungal Infections': {
    description: 'Fungal infections causing itchy rashes.',
    severity: 'mild',
    action: 'Treat with antifungals.',
    treatmentOptions: 'Topical/oral antifungals'
  }
};

  const info = diseaseInfo[topDisease] || {
    description: 'Please consult a dermatologist for proper diagnosis.',
    severity: 'unknown',
    action: 'See a healthcare professional for evaluation.',
    treatmentOptions: 'Consult with dermatologist'
  };

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'serious': return '#dc2626';
      case 'moderate': return '#ea580c';
      case 'mild': return '#f59e0b';
      case 'benign': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getSeverityIcon = (severity) => {
    switch(severity) {
      case 'serious': return <AlertTriangle size={24} />;
      case 'moderate': return <AlertCircle size={24} />;
      case 'benign': return <CheckCircle size={24} />;
      default: return <AlertCircle size={24} />;
    }
  };

  return (
    <div className="disease-results">
      {/* Warning Banner for Low Confidence */}
      {isLowConfidence && (
        <div className="warning-banner">
          <AlertTriangle size={24} />
          <div>
            <h3>Low Confidence Detection</h3>
            <p>{message}</p>
          </div>
        </div>
      )}

      {/* Top Prediction Card */}
      <div className="prediction-card main-prediction">
        <div className="prediction-header">
          <div className="severity-badge" style={{ backgroundColor: getSeverityColor(info.severity) }}>
            {getSeverityIcon(info.severity)}
            <span>{topDisease}</span>
          </div>
        </div>

        <div className="prediction-body">
          <div className="info-section">
            <h4>Description</h4>
            <p>{info.description}</p>
          </div>

          <div className="info-section">
            <h4>Recommended Action</h4>
            <p className="action-text">{info.action}</p>
          </div>

          <div className="info-section">
            <h4>Treatment Options</h4>
            <p>{info.treatmentOptions}</p>
          </div>
        </div>
      </div>


      {/* ABCDE Rule for Melanoma Warning */}
      {(topDisease === 'Melanoma' || topDisease === 'Melanocytic nevus') && (
        <div className="abcde-card">
          <h3>ABCDE Rule for Melanoma Detection</h3>
          <div className="abcde-grid">
            <div className="abcde-item">
              <strong>A</strong>symmetry - One half doesn't match the other
            </div>
            <div className="abcde-item">
              <strong>B</strong>order - Irregular, scalloped, or poorly defined
            </div>
            <div className="abcde-item">
              <strong>C</strong>olor - Varies from one area to another
            </div>
            <div className="abcde-item">
              <strong>D</strong>iameter - Larger than 6mm (pencil eraser)
            </div>
            <div className="abcde-item">
              <strong>E</strong>volving - Changes in size, shape, or color
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="results-actions">
        <button onClick={onReset} className="secondary-btn">
          Analyze Another Image
        </button>
      </div>

      {/* Final Disclaimer */}
      <div className="final-disclaimer">
        <AlertCircle size={20} />
        <div>
          <strong>Important:</strong> This AI analysis is a screening tool only. 
          A definitive diagnosis requires examination by a board-certified dermatologist. 
          {info.severity === 'serious' && (
            <span className="urgent-text"> Seek medical attention promptly.</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default DiseaseResults;