import React, { useState } from 'react';
import { Upload, AlertCircle, Loader2 } from 'lucide-react';
import { analyzeDiseaseImage } from '../services/api';
import DiseaseResults from './Results/DiseaseResults';

const DiseaseDetection = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
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
      setResults(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await analyzeDiseaseImage(selectedImage);
      
      console.log('Disease detection response:', response);
      
      setResults(response);
      
      // Scroll to results
      setTimeout(() => {
        document.getElementById('disease-results')?.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }, 100);
      
    } catch (err) {
      console.error('Disease detection error:', err);
      setError(
        err.response?.data?.error || 
        err.message || 
        'Failed to analyze image. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreview(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="disease-detection-container">
      <div className="disease-detection-content">
        <div className="section-header">
          <h2>Skin Disease Detection</h2>
          <p>Upload a clear image of the affected area for AI-powered analysis</p>
        </div>

        {/* Supported Conditions Notice */}
        <div className="info-card">
          <AlertCircle size={20} />
          <div>
            <h4>Detectable Conditions (10 types)</h4>
            <p>
              Eczema, Warts & Viral Infections, Melanoma, Atopic Dermatitis, 
              Basal Cell Carcinoma (BCC), Melanocytic Nevi (Moles), 
              Benign Keratosis, Psoriasis & Lichen Planus, 
              Seborrheic Keratoses, and Fungal Infections.
            </p>
          </div>
        </div>

        {/* Upload Section */}
        <div className="upload-section">
          <div className="upload-area">
            <input
              type="file"
              id="disease-image-upload"
              accept="image/*"
              onChange={handleImageSelect}
              style={{ display: 'none' }}
            />
            
            {preview ? (
              <div className="image-preview">
                <img src={preview} alt="Selected" />
                <button onClick={handleReset} className="reset-btn">
                  Change Image
                </button>
              </div>
            ) : (
              <label htmlFor="disease-image-upload" className="upload-label">
                <Upload size={48} />
                <span>Click to upload or drag and drop</span>
                <span className="upload-hint">PNG, JPG up to 10MB</span>
              </label>
            )}
          </div>

          {selectedImage && !loading && !results && (
            <button onClick={handleAnalyze} className="analyze-btn">
              Analyze Image
            </button>
          )}

          {loading && (
            <div className="loading-state">
              <Loader2 className="spinner" size={32} />
              <p>Analyzing image...</p>
            </div>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="error-message">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        {/* Results */}
        {results && (
          <div id="disease-results">
            <DiseaseResults results={results} onReset={handleReset} />
          </div>
        )}

        {/* Medical Disclaimer */}
        <div className="disclaimer">
          <AlertCircle size={18} />
          <p>
            <strong>Medical Disclaimer:</strong> This tool is for informational purposes only 
            and is not a substitute for professional medical advice, diagnosis, or treatment. 
            Always consult a qualified dermatologist for accurate diagnosis and treatment.
          </p>
        </div>
      </div>
    </div>
  );
};

export default DiseaseDetection;