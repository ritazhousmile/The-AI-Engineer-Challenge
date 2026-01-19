import React, { useState, useRef, useEffect } from 'react';
import './Widget.css';

/**
 * Mental Coach AI Chatbot Widget
 * 
 * Usage:
 *   <MentalCoachWidget apiUrl="https://your-api.com" apiKey="optional-key" />
 */
const MentalCoachWidget = ({ 
  apiUrl = 'http://localhost:8000',
  apiKey = null,
  primaryColor = '#6366f1',
  position = 'bottom-right'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (isOpen && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  const sendMessage = async (e) => {
    e?.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentMessage = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    // Create placeholder for assistant response
    const assistantMessageIndex = messages.length + 1;
    setMessages(prev => [...prev, {
      role: 'assistant',
      content: '',
      timestamp: new Date()
    }]);

    try {
      const headers = {
        'Content-Type': 'application/json'
      };
      if (apiKey) {
        headers['Authorization'] = `Bearer ${apiKey}`;
      }

      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          message: currentMessage,
          conversation_id: conversationId
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let accumulatedContent = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));
                
                if (data.error) {
                  setMessages(prev => {
                    const newMessages = [...prev];
                    newMessages[assistantMessageIndex] = {
                      ...newMessages[assistantMessageIndex],
                      content: `Error: ${data.error}`
                    };
                    return newMessages;
                  });
                  break;
                }
                
                if (data.content) {
                  accumulatedContent += data.content;
                  setMessages(prev => {
                    const newMessages = [...prev];
                    newMessages[assistantMessageIndex] = {
                      ...newMessages[assistantMessageIndex],
                      content: accumulatedContent
                    };
                    return newMessages;
                  });
                }
                
                if (data.conversation_id && !conversationId) {
                  setConversationId(data.conversation_id);
                }
                
                if (data.done) {
                  if (data.conversation_id) {
                    setConversationId(data.conversation_id);
                  }
                  break;
                }
              } catch (e) {
                console.warn('Failed to parse chunk:', e);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[assistantMessageIndex] = {
          ...newMessages[assistantMessageIndex],
          content: 'Sorry, I encountered an error. Please try again.'
        };
        return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setConversationId(null);
  };

  const positionClasses = {
    'bottom-right': 'widget-bottom-right',
    'bottom-left': 'widget-bottom-left',
    'top-right': 'widget-top-right',
    'top-left': 'widget-top-left'
  };

  return (
    <div className={`mental-coach-widget ${positionClasses[position] || positionClasses['bottom-right']}`}>
      {/* Chat Button */}
      {!isOpen && (
        <button
          className="widget-toggle-button"
          onClick={() => setIsOpen(true)}
          style={{ backgroundColor: primaryColor }}
          aria-label="Open chat"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="widget-container">
          {/* Header */}
          <div className="widget-header" style={{ backgroundColor: primaryColor }}>
            <div className="widget-header-content">
              <span className="widget-title">🧠 Mental Coach AI</span>
              <div className="widget-header-actions">
                {messages.length > 0 && (
                  <button
                    className="widget-icon-button"
                    onClick={clearChat}
                    aria-label="Clear chat"
                    title="Clear chat"
                  >
                    🗑️
                  </button>
                )}
                <button
                  className="widget-icon-button"
                  onClick={() => setIsOpen(false)}
                  aria-label="Close chat"
                  title="Close chat"
                >
                  ✕
                </button>
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="widget-messages">
            {messages.length === 0 ? (
              <div className="widget-welcome">
                <div className="widget-welcome-icon">🌟</div>
                <h3>Welcome to Mental Coach AI</h3>
                <p>I'm here to support you. Share what's on your mind, and let's work through it together.</p>
                <div className="widget-suggestions">
                  {[
                    "I'm feeling overwhelmed",
                    "I need help staying motivated",
                    "I want to build better habits"
                  ].map((suggestion, idx) => (
                    <button
                      key={idx}
                      className="widget-suggestion-button"
                      onClick={() => {
                        setInputMessage(suggestion);
                        setTimeout(() => sendMessage(), 100);
                      }}
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={index}
                  className={`widget-message widget-message-${message.role}`}
                >
                  <div className="widget-message-content">
                    {message.content || (isLoading && index === messages.length - 1 ? '...' : '')}
                  </div>
                </div>
              ))
            )}
            {isLoading && messages.length > 0 && (
              <div className="widget-typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form className="widget-input-container" onSubmit={sendMessage}>
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading}
              className="widget-input"
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || isLoading}
              className="widget-send-button"
              style={{ backgroundColor: primaryColor }}
              aria-label="Send message"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default MentalCoachWidget;
