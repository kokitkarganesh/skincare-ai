import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
  timeout: 60000, // 60 seconds for model inference
});

// Disease Detection API
export const analyzeDiseaseImage = async (imageFile) => {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);

    console.log('Sending disease detection request...');
    
    const response = await api.post('/api/disease/analyze', formData);
    
    console.log('Disease detection response:', response.data);
    
    return response.data;
  } catch (error) {
    console.error('Disease detection API error:', error);
    
    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data.error || error.response.data.message || 'Analysis failed');
    } else if (error.request) {
      // Request made but no response
      throw new Error('No response from server. Please check your connection.');
    } else {
      // Error setting up request
      throw new Error(error.message || 'Failed to analyze image');
    }
  }
};

// Get available disease classes
export const getDiseaseClasses = async () => {
  try {
    const response = await api.get('/api/disease/classes');
    return response.data;
  } catch (error) {
    console.error('Get classes error:', error);
    throw error;
  }
};

// Skincare Analysis API
export const analyzeSkincareImage = async (imageFile, questionnaire) => {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('questionnaire', JSON.stringify(questionnaire));

    console.log('Sending skincare analysis request...');
    
    const response = await api.post('/api/skincare/analyze', formData);
    
    console.log('Skincare analysis response:', response.data);
    
    return response.data;
  } catch (error) {
    console.error('Skincare analysis API error:', error);
    
    if (error.response) {
      throw new Error(error.response.data.error || 'Analysis failed');
    } else if (error.request) {
      throw new Error('No response from server. Please check your connection.');
    } else {
      throw new Error(error.message || 'Failed to analyze image');
    }
  }
};

// Chatbot API
export const sendChatMessage = async (message, conversationHistory = [], skinType = null) => {
  try {
    console.log('Sending chat message:', message);
    
    const response = await api.post('/api/chatbot/chat', {
      message: message,
      skin_type: skinType  // Backend expects 'skin_type', not 'conversation_history'
    }, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    console.log('Chat response:', response.data);
    
    // Backend returns: { success, message, source, similarity_score, matched_question, confidence }
    return {
      response: response.data.message,  // Map 'message' to 'response' for frontend
      source: response.data.source,
      confidence: response.data.confidence,
      matched_question: response.data.matched_question,
      similarity_score: response.data.similarity_score
    };
  } catch (error) {
    console.error('Chatbot API error:', error);
    
    if (error.response) {
      throw new Error(error.response.data.error || 'Chat failed');
    } else if (error.request) {
      throw new Error('No response from server');
    } else {
      throw new Error(error.message || 'Failed to send message');
    }
  }
};

// Health check
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check error:', error);
    throw error;
  }
};

export default api;