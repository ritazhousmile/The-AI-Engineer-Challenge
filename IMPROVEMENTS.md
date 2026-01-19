# 🚀 Chatbot Improvements & Integration Guide

## Overview

This document outlines the improvements made to the Mental Coach AI chatbot and how to integrate it with other systems.

---

## ✨ Key Improvements

### 1. **Conversation History Management**
- ✅ Persistent conversation storage using SQLite database
- ✅ Context-aware responses that remember previous messages
- ✅ Conversation ID tracking for multi-session support
- ✅ Retrieve and manage conversation history via API

**Benefits:**
- Users can have meaningful, context-aware conversations
- Conversations persist across sessions
- Better user experience with continuity

### 2. **Database Storage**
- ✅ SQLite database for conversation storage
- ✅ Automatic database initialization
- ✅ Efficient indexing for fast queries
- ✅ Conversation and message tracking

**Database Schema:**
- `conversations` table: Stores conversation metadata
- `messages` table: Stores all messages with roles (user/assistant)

### 3. **API Authentication**
- ✅ Optional API key authentication
- ✅ Bearer token support
- ✅ Configurable via environment variables
- ✅ Can be disabled for development

**Setup:**
```bash
export API_KEY=your-secure-api-key-here
```

### 4. **Rate Limiting**
- ✅ Configurable rate limiting per IP address
- ✅ Default: 60 requests per 60 seconds
- ✅ Prevents API abuse
- ✅ Customizable via environment variables

**Configuration:**
```bash
export RATE_LIMIT_ENABLED=true
export RATE_LIMIT_REQUESTS=60
export RATE_LIMIT_WINDOW=60
```

### 5. **Enhanced Error Handling**
- ✅ Global exception handler
- ✅ User-friendly error messages
- ✅ Detailed logging for debugging
- ✅ Proper HTTP status codes
- ✅ Error context in responses

### 6. **Health Check & Monitoring**
- ✅ `/api/health` endpoint
- ✅ Database connection status
- ✅ OpenAI configuration status
- ✅ API version information

### 7. **Integration Endpoints**
- ✅ Webhook endpoint for external systems
- ✅ RESTful conversation management
- ✅ Support for custom system prompts
- ✅ Multiple integration examples

### 8. **Improved CORS Configuration**
- ✅ Configurable allowed origins
- ✅ Support for credentials
- ✅ Environment-based configuration

---

## 🔌 Integration Options

### 1. REST API Integration
**Best for:** Web applications, mobile apps, server-to-server communication

**Features:**
- Streaming responses (Server-Sent Events)
- Conversation history support
- Custom system prompts
- Full conversation management

**Example:**
```javascript
const response = await fetch('https://your-api.com/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    message: 'Hello!',
    conversation_id: 'user-123'
  })
});
```

### 2. Webhook Integration
**Best for:** Slack, Discord, WhatsApp, Telegram bots

**Features:**
- Synchronous responses
- Simple request/response model
- Webhook callback support (future)

**Example:**
```python
response = requests.post(
    'https://your-api.com/api/webhook',
    json={
        'message': 'User message',
        'conversation_id': 'user-123'
    },
    headers={'Authorization': 'Bearer YOUR_API_KEY'}
)
```

### 3. Embeddable Widget
**Best for:** Websites, landing pages, customer support

**Features:**
- Easy to embed
- Customizable styling
- Conversation persistence
- No backend required

### 4. SDK Integration
**Best for:** Python/JavaScript applications

**Features:**
- Type-safe clients
- Simplified API calls
- Built-in error handling
- Conversation management

---

## 📊 API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/health` | GET | Health check | No |
| `/api/chat` | POST | Stream chat (SSE) | Optional |
| `/api/conversations/{id}` | GET | Get conversation | Optional |
| `/api/conversations/{id}` | DELETE | Delete conversation | Optional |
| `/api/webhook` | POST | Webhook integration | Optional |

---

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-your-openai-key

# Optional - Authentication
API_KEY=your-api-key-for-protection

# Optional - Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_WINDOW=60

# Optional - CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Optional - Database
DB_PATH=conversations.db

# Optional - Debugging
DEBUG=false
```

---

## 🚀 Quick Start Integration

### Python Example

```python
import requests

API_URL = "https://your-api.com"
API_KEY = "your-api-key"

# Send a message
response = requests.post(
    f"{API_URL}/api/webhook",
    json={
        "message": "I need help with stress",
        "conversation_id": "user-123"
    },
    headers={"Authorization": f"Bearer {API_KEY}"}
)

result = response.json()
print(result["response"])
```

### JavaScript Example

```javascript
async function chat(message, conversationId) {
  const response = await fetch('https://your-api.com/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_API_KEY'
    },
    body: JSON.stringify({
      message: message,
      conversation_id: conversationId
    })
  });

  // Handle streaming response
  const reader = response.body.getReader();
  // ... (see INTEGRATION_GUIDE.md for full example)
}
```

---

## 📚 Documentation

- **Full Integration Guide**: See `INTEGRATION_GUIDE.md`
- **API Documentation**: Available at `/docs` (Swagger UI) when server is running
- **Examples**: See `INTEGRATION_GUIDE.md` for platform-specific examples

---

## 🔒 Security Best Practices

1. **Always use HTTPS** in production
2. **Set API_KEY** for authentication
3. **Configure CORS** to restrict origins
4. **Enable rate limiting** to prevent abuse
5. **Monitor health endpoint** regularly
6. **Keep API keys secure** - never commit to version control

---

## 🎯 Use Cases

### 1. Customer Support
- Embed widget on website
- Provide 24/7 support
- Maintain conversation context

### 2. Mental Health Apps
- Integrate into mobile apps
- Track user conversations
- Provide personalized coaching

### 3. Slack/Discord Bots
- Team mental wellness support
- Anonymous help channels
- Group coaching sessions

### 4. Educational Platforms
- Student support chatbot
- Study motivation coach
- Learning companion

### 5. Healthcare Platforms
- Pre-screening tool
- Wellness check-ins
- Resource recommendations

---

## 📈 Next Steps

### Recommended Enhancements

1. **Redis Integration** - Replace in-memory rate limiting with Redis
2. **PostgreSQL Support** - For production-scale deployments
3. **Analytics Dashboard** - Track usage and conversations
4. **Multi-language Support** - Support multiple languages
5. **Voice Integration** - Add voice input/output
6. **Sentiment Analysis** - Analyze user sentiment
7. **Export Conversations** - Allow users to export their data
8. **Admin Dashboard** - Manage conversations and users

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Rate limit errors
- **Solution**: Adjust `RATE_LIMIT_REQUESTS` or disable temporarily

**Issue**: Database errors
- **Solution**: Check file permissions for `conversations.db`

**Issue**: CORS errors
- **Solution**: Configure `ALLOWED_ORIGINS` environment variable

**Issue**: Authentication errors
- **Solution**: Verify `API_KEY` is set correctly

---

## 📞 Support

For integration help, see:
- `INTEGRATION_GUIDE.md` - Comprehensive integration examples
- API docs at `/docs` - Interactive API documentation
- Health endpoint at `/api/health` - System status

---

**Version**: 2.0.0  
**Last Updated**: 2024
