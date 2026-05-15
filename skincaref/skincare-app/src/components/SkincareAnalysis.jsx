import React, { useState } from 'react';
import { Upload, AlertCircle, Loader2 } from 'lucide-react';
import { analyzeSkincareImage } from '../services/api';
import Questionnaire from './Questionnaire';
import SkincareResults from './Results/SkincareResults';

const SkincareAnalysis = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [showQuestionnaire, setShowQuestionnaire] = useState(false);
  const [questionnaire, setQuestionnaire] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setError('Please select a valid image file');
        return;
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('Image size must be less than 10MB');
        return;
      }

      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setError(null);
      setShowQuestionnaire(false);
      setResults(null);
    }
  };

  const handleContinue = () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }
    setShowQuestionnaire(true);
  };

  const handleQuestionnaireComplete = async (answers) => {
    setQuestionnaire(answers);
    setLoading(true);
    setError(null);

    try {
      const response = await analyzeSkincareImage(selectedImage, answers);
      
      console.log('Skincare analysis response:', response);
      
      setResults(response);
      
      // Scroll to results
      setTimeout(() => {
        document.getElementById('skincare-results')?.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }, 100);
      
    } catch (err) {
      console.error('Skincare analysis error:', err);
      setError(
        err.response?.data?.error || 
        err.message || 
        'Failed to analyze. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreview(null);
    setShowQuestionnaire(false);
    setQuestionnaire(null);
    setResults(null);
    setError(null);
  };

  if (results) {
    return (
      <div id="skincare-results">
        <SkincareResults 
          results={results} 
          questionnaire={questionnaire}
          onReset={handleReset} 
        />
      </div>
    );
  }

  if (showQuestionnaire) {
    return (
      <Questionnaire
        onSubmit={handleQuestionnaireComplete}
        onBack={() => setShowQuestionnaire(false)}
        loading={loading}
      />
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Skincare Analysis</h1>
        <p>Upload a photo for personalized skincare recommendations</p>
      </div>

      <div className="upload-section">
        {/* Upload Area */}
        <div className="upload-card">
          <input
            type="file"
            id="skincare-image-upload"
            accept="image/*"
            onChange={handleImageSelect}
            style={{ display: 'none' }}
          />
          
          {preview ? (
            <div className="image-preview-container">
              <img src={preview} alt="Preview" className="image-preview" />
              <button onClick={handleReset} className="btn-secondary">
                Change Image
              </button>
            </div>
          ) : (
            <label htmlFor="skincare-image-upload" className="upload-area">
              <div className="upload-icon">
                <Upload size={32} />
              </div>
              <h3>Upload Your Photo</h3>
              <p>Clear, well-lit photo works best</p>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                PNG, JPG up to 10MB
              </p>
            </label>
          )}
        </div>

        {/* Continue Button */}
        {selectedImage && !loading && (
          <button onClick={handleContinue} className="btn-primary btn-large">
            Continue to Questionnaire
          </button>
        )}

        {/* Error Display */}
        {error && (
          <div className="alert alert-error">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Info Cards */}
      <div style={{ maxWidth: '600px', margin: '3rem auto 0' }}>
        <div className="info-card">
          <AlertCircle size={20} />
          <div>
            <h4>What We Analyze</h4>
            <p>
              Our AI analyzes your skin type (Dry, Normal, Oily) and provides 
              personalized routines, product recommendations, and lifestyle tips 
              based on your concerns.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SkincareAnalysis;