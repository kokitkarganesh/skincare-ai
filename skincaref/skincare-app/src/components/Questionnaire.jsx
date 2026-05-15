import React, { useState } from 'react';
import { ChevronLeft, Sparkles } from 'lucide-react';

const Questionnaire = ({ onSubmit, onBack, loading }) => {
  const [formData, setFormData] = useState({
    concerns: [],
    sleep_hours: '',
    water_intake: '',
    stress_level: '',
    sun_exposure: '',
    diet: ''
  });

  const concernOptions = [
    'Acne',
    'Dark Circles',
    'Pigmentation',
    'Wrinkles',
    'Redness',
    'Large Pores',
    'Dryness',
    'Oiliness'
  ];

  const handleConcernToggle = (concern) => {
    setFormData(prev => ({
      ...prev,
      concerns: prev.concerns.includes(concern)
        ? prev.concerns.filter(c => c !== concern)
        : [...prev.concerns, concern]
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="questionnaire-container">
      <button className="btn-back" onClick={onBack}>
        <ChevronLeft size={20} />
        Back to Upload
      </button>

      <h2>Tell Us About Your Skin</h2>
      <p className="questionnaire-subtitle">
        This helps us personalize your skincare routine
      </p>

      <form onSubmit={handleSubmit} className="questionnaire-form">
        
        {/* Skin Concerns */}
        <div className="form-section">
          <label className="form-label">What are your main skin concerns? (Select all that apply)</label>
          <div className="concern-grid">
            {concernOptions.map(concern => (
              <button
                key={concern}
                type="button"
                className={`concern-chip ${formData.concerns.includes(concern) ? 'selected' : ''}`}
                onClick={() => handleConcernToggle(concern)}
              >
                {concern}
              </button>
            ))}
          </div>
        </div>

        {/* Sleep Hours */}
        <div className="form-section">
          <label className="form-label">How many hours do you sleep per night?</label>
          <select
            value={formData.sleep_hours}
            onChange={(e) => setFormData({...formData, sleep_hours: e.target.value})}
            className="form-select"
          >
            <option value="">Select...</option>
            <option value="Less than 5 hours">Less than 5 hours</option>
            <option value="5-6 hours">5-6 hours</option>
            <option value="7-8 hours">7-8 hours ✨ Ideal</option>
            <option value="More than 8 hours">More than 8 hours</option>
          </select>
        </div>

        {/* Water Intake */}
        <div className="form-section">
          <label className="form-label">How much water do you drink daily?</label>
          <select
            value={formData.water_intake}
            onChange={(e) => setFormData({...formData, water_intake: e.target.value})}
            className="form-select"
          >
            <option value="">Select...</option>
            <option value="Less than 3 glasses">Less than 3 glasses</option>
            <option value="3-5 glasses">3-5 glasses</option>
            <option value="6-7 glasses">6-7 glasses</option>
            <option value="8+ glasses">8+ glasses ✨ Ideal</option>
          </select>
        </div>

        {/* Stress Level */}
        <div className="form-section">
          <label className="form-label">What's your stress level?</label>
          <select
            value={formData.stress_level}
            onChange={(e) => setFormData({...formData, stress_level: e.target.value})}
            className="form-select"
          >
            <option value="">Select...</option>
            <option value="Low">Low</option>
            <option value="Moderate">Moderate</option>
            <option value="High">High</option>
            <option value="Very high">Very high</option>
          </select>
        </div>

        {/* Sun Exposure */}
        <div className="form-section">
          <label className="form-label">How much sun exposure do you get?</label>
          <select
            value={formData.sun_exposure}
            onChange={(e) => setFormData({...formData, sun_exposure: e.target.value})}
            className="form-select"
          >
            <option value="">Select...</option>
            <option value="Low">Low (mostly indoors)</option>
            <option value="Moderate">Moderate (some outdoor time)</option>
            <option value="High">High (frequent outdoor activities)</option>
          </select>
        </div>

        {/* Diet */}
        <div className="form-section">
          <label className="form-label">How would you describe your diet?</label>
          <select
            value={formData.diet}
            onChange={(e) => setFormData({...formData, diet: e.target.value})}
            className="form-select"
          >
            <option value="">Select...</option>
            <option value="Balanced">Balanced & nutritious</option>
            <option value="Mixed">Mixed</option>
            <option value="Fast food / Processed">Fast food / Processed</option>
            <option value="Vegetarian">Vegetarian</option>
            <option value="Vegan">Vegan</option>
            <option value="Keto">Keto</option>
          </select>
        </div>

        <button 
          type="submit" 
          className="btn-primary btn-large"
          disabled={loading}
        >
          {loading ? (
            'Analyzing...'
          ) : (
            <>
              Get My Personalized Routine
              <Sparkles size={20} />
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default Questionnaire;