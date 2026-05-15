import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';
import { sendChatMessage } from '../services/api';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content: 'Hi! I\'m your AI skincare assistant powered by advanced RAG technology. Ask me anything about skincare routines, ingredients, or concerns!',
      timestamp: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [selectedSkinType, setSelectedSkinType] = useState('normal');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const quickQuestions = [
    'How to treat acne?',
    'Best morning routine?',
    'Remove dark circles?',
    'Reduce wrinkles?',
    'Oily skin tips?',
    'What is retinol?'
  ];

  const handleQuickQuestion = (question) => {
    setInput(question);
    inputRef.current?.focus();
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      // Send message with skin type (backend doesn't use conversation history)
      const response = await sendChatMessage(
        userMessage.content,
        [], // Not used by backend, but keeping for compatibility
        selectedSkinType
      );

      const botMessage = {
        role: 'bot',
        content: response.response || 'I apologize, but I couldn\'t process that. Could you rephrase?',
        confidence: response.confidence,
        source: response.source,
        matched_question: response.matched_question,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      
      const errorMessage = {
        role: 'bot',
        content: 'Sorry, I encountered an error. Please try again or rephrase your question.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>AI Skincare Assistant</h1>
        <p>Get instant answers to your skincare questions</p>
      </div>

      <div className="chatbot-container">
        {/* Header */}
        <div className="chatbot-header">
          <h2>
            <Bot size={24} style={{ display: 'inline', marginRight: '0.5rem' }} />
            Skincare Expert
          </h2>
          <p>Powered by RAG + Gemini</p>
        </div>

        {/* Skin Type Selector */}
        <div className="skin-type-selector">
          <label>My skin type:</label>
          <select
            value={selectedSkinType}
            onChange={(e) => setSelectedSkinType(e.target.value)}
            className="skin-type-select"
          >
            <option value="dry">Dry</option>
            <option value="normal">Normal</option>
            <option value="oily">Oily</option>
            <option value="combination">Combination</option>
            <option value="sensitive">Sensitive</option>
          </select>
        </div>

        {/* Quick Questions */}
        {messages.length <= 1 && (
          <div className="quick-questions">
            <h4>Quick Questions</h4>
            <div className="quick-questions-grid">
              {quickQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickQuestion(question)}
                  className="quick-question-btn"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-avatar">
                {message.role === 'bot' ? <Bot size={20} /> : <User size={20} />}
              </div>
              <div className="message-content">
                <div className="message-bubble">
                  {message.content.split('\n').map((line, i) => (
                    <p key={i}>{line}</p>
                  ))}
                </div>
                <span className="message-meta">
                  {new Date(message.timestamp).toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </span>
              </div>
            </div>
          ))}

          {/* Typing Indicator */}
          {isTyping && (
            <div className="message bot">
              <div className="message-avatar">
                <Bot size={20} />
              </div>
              <div className="message-content">
                <div className="message-bubble typing">
                  <div className="loading-spinner" />
                  <span>Analyzing knowledge base...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="chat-input-container">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about routines, ingredients, treatments..."
            className="chat-input"
            rows={1}
            disabled={isTyping}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            className="send-btn"
          >
            <Send size={20} />
          </button>
        </div>
      </div>

      {/* Info */}
      <div style={{ maxWidth: '900px', margin: '2rem auto 0' }}>
        <div className="info-card">
          <Sparkles size={20} />
          <div>
            <h4>How It Works</h4>
            <p>
              Our AI assistant uses RAG (Retrieval-Augmented Generation) with FAISS vector search 
              and Gemini. It searches through 175+ expert skincare Q&As to provide 
              accurate, personalized advice based on your skin type. Ask about specific concerns, 
              product recommendations, routines, or ingredients!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;