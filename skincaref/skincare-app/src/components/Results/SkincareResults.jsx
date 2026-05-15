import React, { useState } from 'react';
import { Sparkles, RefreshCw, Sun, Moon, Calendar, Heart, AlertCircle } from 'lucide-react';
import RoutineCard from './RoutineCard';

const SkincareResults = ({ results, onStartOver }) => {
  const [activeTab, setActiveTab] = useState('routine');
  const { ai_analysis, personalized_routine, concern_specific_advice, user_input } = results;

  return (
    <div className="skincare-results">
      {/* Header */}
      <div className="results-header success">
        <Sparkles size={32} />
        <h2>Your Personalized Skincare Routine</h2>
        <p>Based on AI analysis and your lifestyle</p>
      </div>

      {/* Skin Type Badge */}
      <div className="skin-type-badge">
        <div className="skin-type-info">
          <h3>Detected Skin Type : {ai_analysis.skin_type} Skin</h3>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'routine' ? 'active' : ''}`}
          onClick={() => setActiveTab('routine')}
        >
          <Sparkles size={18} />
          Routine
        </button>
        {concern_specific_advice && concern_specific_advice.length > 0 && (
          <button 
            className={`tab ${activeTab === 'concerns' ? 'active' : ''}`}
            onClick={() => setActiveTab('concerns')}
          >
            <Heart size={18} />
            Concern Advice ({concern_specific_advice.length})
          </button>
        )}
        <button 
          className={`tab ${activeTab === 'lifestyle' ? 'active' : ''}`}
          onClick={() => setActiveTab('lifestyle')}
        >
          <Sun size={18} />
          Lifestyle Tips
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        
        {/* Routine Tab */}
        {activeTab === 'routine' && (
          <div className="routine-content">
            <RoutineCard 
              title="Morning Routine"
              icon={<Sun size={24} />}
              steps={personalized_routine.morning}
              color="morning"
            />
            
            <RoutineCard 
              title="Evening Routine"
              icon={<Moon size={24} />}
              steps={personalized_routine.evening}
              color="evening"
            />

            <RoutineCard 
              title="Weekly Treatments"
              icon={<Calendar size={24} />}
              treatments={personalized_routine.weekly_treatments}
              color="weekly"
            />

            {/* Wellness Tips */}
            <div className="wellness-section">
              <h3>✨ Wellness Tips</h3>
              <div className="wellness-grid">
                {personalized_routine.wellness_tips.map((tip, index) => (
                  <div key={index} className="wellness-tip">
                    {tip}
                  </div>
                ))}
              </div>
            </div>

            {/* Things to Avoid */}
            <div className="avoid-section">
              <h3>⚠️ Avoid</h3>
              <div className="avoid-list">
                {personalized_routine.avoid.map((item, index) => (
                  <span key={index} className="avoid-tag">{item}</span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Concerns Tab */}
        {activeTab === 'concerns' && concern_specific_advice && (
          <div className="concerns-content">
            {concern_specific_advice.map((advice, index) => (
              <div key={index} className="concern-advice-card">
                <div className="concern-header">
                  <h3>{advice.concern}</h3>
                  <span className={`confidence-badge ${advice.confidence}`}>
                    {advice.source === 'stored' ? '✨ Expert Advice' : '🤖 AI Generated'}
                  </span>
                </div>
                <div className="concern-advice-content">
                  {advice.advice.split('\n').map((line, i) => (
                    <p key={i}>{line}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Lifestyle Tab */}
        {activeTab === 'lifestyle' && (
          <div className="lifestyle-content">
            {personalized_routine.lifestyle_tips && personalized_routine.lifestyle_tips.length > 0 ? (
              personalized_routine.lifestyle_tips.map((tip, index) => (
                <div key={index} className="lifestyle-tip-card">
                  <div className="lifestyle-issue">
                    <AlertCircle size={20} />
                    <h4>{tip.issue}</h4>
                  </div>
                  <p className="impact"><strong>Impact:</strong> {tip.impact}</p>
                  <p className="recommendation"><strong>Recommendation:</strong> {tip.recommendation}</p>
                  <p className="remedy"><strong>Natural Remedy:</strong> {tip.natural_remedy}</p>
                </div>
              ))
            ) : (
              <div className="no-lifestyle-tips">
                <Sparkles size={48} />
                <h3>Great job! 🎉</h3>
                <p>Your lifestyle habits are well-balanced. Keep it up!</p>
              </div>
            )}

            {/* Diet Tips */}
            <div className="diet-tips-section">
              <h3>🥗 Diet Tips for {ai_analysis.skin_type} Skin</h3>
              <ul className="diet-tips-list">
                {personalized_routine.diet_tips.map((tip, index) => (
                  <li key={index}>{tip}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* Start Over Button */}
      <button className="btn-secondary btn-large" onClick={onStartOver}>
        <RefreshCw size={20} />
        Start New Analysis
      </button>
    </div>
  );
};

export default SkincareResults;