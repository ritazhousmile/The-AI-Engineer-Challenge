# 🔌 Integration Guide - Mental Coach AI Chatbot

This guide explains how to integrate the Mental Coach AI chatbot with other systems and applications.

## 📋 Table of Contents

1. [API Overview](#api-overview)
2. [REST API Integration](#rest-api-integration)
3. [Webhook Integration](#webhook-integration)
4. [Embeddable Widget](#embeddable-widget)
5. [SDK Examples](#sdk-examples)
6. [Platform-Specific Integrations](#platform-specific-integrations)
7. [Authentication](#authentication)

---

## 🌐 API Overview

### Base URL
- **Production**: `https://your-api-domain.vercel.app`
- **Development**: `http://localhost:8000`

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check and system status |
| `/api/chat` | POST | Stream chat responses (SSE) |
| `/api/conversations/{id}` | GET | Retrieve conversation history |
| `/api/conversations/{id}` | DELETE | Delete a conversation |
| `/api/webhook` | POST | Webhook endpoint for external systems |

### API Version
Current version: **2.0.0**

---

## 🔗 REST API Integration

### 1. Basic Chat Request

**Endpoint**: `POST /api/chat`

**Request Body**:
```json
{
  "message": "I'm feeling overwhelmed today",
  "conversation_id": "optional-conversation-id",
  "system_prompt": "optional-custom-prompt"
}
```

**Response**: Server-Sent Events (SSE) stream

**Example (cURL)**:
```bash
curl -X POST https://your-api-domain.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "message": "I need help with stress management",
    "conversation_id": "user-123-session-1"
  }'
```

**Example (JavaScript/TypeScript)**:
```javascript
async function sendMessage(message, conversationId = null) {
  const response = await fetch('https://your-api-domain.vercel.app/api/chat', {
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

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let fullResponse = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        if (data.content) {
          fullResponse += data.content;
          // Update UI in real-time
          console.log('Streaming:', fullResponse);
        }
        if (data.done) {
          console.log('Complete response:', fullResponse);
          return { response: fullResponse, conversationId: data.conversation_id };
        }
      }
    }
  }
}
```

**Example (Python)**:
```python
import requests
import json

def send_message(message, conversation_id=None, api_key=None):
    url = "https://your-api-domain.vercel.app/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    data = {
        "message": message,
        "conversation_id": conversation_id
    }
    
    response = requests.post(url, json=data, headers=headers, stream=True)
    
    full_response = ""
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            if line_str.startswith('data: '):
                data = json.loads(line_str[6:])
                if 'content' in data:
                    full_response += data['content']
                    print(full_response, end='\r')
                if data.get('done'):
                    return {
                        'response': full_response,
                        'conversation_id': data.get('conversation_id')
                    }
    return {'response': full_response}
```

### 2. Retrieve Conversation History

**Endpoint**: `GET /api/conversations/{conversation_id}`

**Example**:
```bash
curl -X GET https://your-api-domain.vercel.app/api/conversations/user-123-session-1 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response**:
```json
{
  "conversation_id": "user-123-session-1",
  "messages": [
    {
      "role": "user",
      "content": "I'm feeling overwhelmed",
      "timestamp": "2024-01-15T10:30:00"
    },
    {
      "role": "assistant",
      "content": "I understand that feeling overwhelmed can be really challenging...",
      "timestamp": "2024-01-15T10:30:15"
    }
  ],
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:35:00"
}
```

---

## 🪝 Webhook Integration

The webhook endpoint allows external systems to send messages and receive responses synchronously.

**Endpoint**: `POST /api/webhook`

**Request Body**:
```json
{
  "message": "User message from external system",
  "conversation_id": "optional-conversation-id",
  "webhook_url": "https://your-system.com/webhook-callback"
}
```

**Response**:
```json
{
  "conversation_id": "generated-or-provided-id",
  "response": "AI assistant response",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Example (Slack Bot Integration)**:
```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
CHATBOT_API = "https://your-api-domain.vercel.app/api/webhook"
API_KEY = "your-api-key"

@app.route('/slack/events', methods=['POST'])
def slack_event():
    data = request.json
    if data.get('type') == 'url_verification':
        return jsonify({'challenge': data['challenge']})
    
    event = data.get('event', {})
    if event.get('type') == 'message' and 'bot_id' not in event:
        user_message = event.get('text')
        user_id = event.get('user')
        conversation_id = f"slack-{user_id}"
        
        # Call chatbot API
        response = requests.post(
            CHATBOT_API,
            json={
                "message": user_message,
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        
        bot_response = response.json()
        
        # Send response back to Slack
        # (Implementation depends on Slack API setup)
        
    return jsonify({'status': 'ok'})
```

---

## 🎨 Embeddable Widget

Create an embeddable chat widget for your website:

**HTML**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Mental Coach Widget</title>
    <style>
        #chatbot-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            height: 500px;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            background: white;
        }
        #chatbot-messages {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
        }
        #chatbot-input {
            display: flex;
            padding: 10px;
            border-top: 1px solid #eee;
        }
        #chatbot-input input {
            flex: 1;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        #chatbot-input button {
            margin-left: 10px;
            padding: 8px 15px;
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div id="chatbot-widget">
        <div id="chatbot-messages"></div>
        <div id="chatbot-input">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const API_URL = 'https://your-api-domain.vercel.app';
        const API_KEY = 'your-api-key';
        let conversationId = null;

        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;

            addMessage('user', message);
            input.value = '';

            try {
                const response = await fetch(`${API_URL}/api/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${API_KEY}`
                    },
                    body: JSON.stringify({
                        message: message,
                        conversation_id: conversationId
                    })
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let assistantMessage = addMessage('assistant', '');

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\n');

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = JSON.parse(line.slice(6));
                            if (data.content) {
                                assistantMessage.textContent += data.content;
                            }
                            if (data.conversation_id) {
                                conversationId = data.conversation_id;
                            }
                        }
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                addMessage('assistant', 'Sorry, I encountered an error.');
            }
        }

        function addMessage(role, content) {
            const messagesDiv = document.getElementById('chatbot-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            messageDiv.textContent = content;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            return messageDiv;
        }

        document.getElementById('user-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
```

---

## 📦 SDK Examples

### Python SDK

```python
# mental_coach_sdk.py
import requests
import json

class MentalCoachClient:
    def __init__(self, api_url, api_key=None):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.conversation_id = None
    
    def chat(self, message, stream=True):
        """Send a message and get response"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        data = {
            "message": message,
            "conversation_id": self.conversation_id
        }
        
        response = requests.post(
            f"{self.api_url}/api/chat",
            json=data,
            headers=headers,
            stream=stream
        )
        
        if stream:
            return self._handle_stream(response)
        else:
            return response.json()
    
    def _handle_stream(self, response):
        """Handle streaming response"""
        full_response = ""
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data = json.loads(line_str[6:])
                    if 'content' in data:
                        full_response += data['content']
                        yield data['content']
                    if data.get('conversation_id'):
                        self.conversation_id = data['conversation_id']
                    if data.get('done'):
                        break
        return full_response
    
    def get_conversation(self, conversation_id=None):
        """Retrieve conversation history"""
        conv_id = conversation_id or self.conversation_id
        if not conv_id:
            raise ValueError("No conversation ID provided")
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        response = requests.get(
            f"{self.api_url}/api/conversations/{conv_id}",
            headers=headers
        )
        return response.json()

# Usage
client = MentalCoachClient(
    api_url="https://your-api-domain.vercel.app",
    api_key="your-api-key"
)

# Stream response
for chunk in client.chat("I'm feeling anxious"):
    print(chunk, end='', flush=True)

# Get conversation history
history = client.get_conversation()
print(history)
```

### JavaScript/TypeScript SDK

```typescript
// mental-coach-sdk.ts
export class MentalCoachClient {
  private apiUrl: string;
  private apiKey?: string;
  private conversationId?: string;

  constructor(apiUrl: string, apiKey?: string) {
    this.apiUrl = apiUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
  }

  async chat(
    message: string,
    onChunk?: (chunk: string) => void
  ): Promise<{ response: string; conversationId: string }> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(`${this.apiUrl}/api/chat`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        message,
        conversation_id: this.conversationId,
      }),
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let fullResponse = '';

    if (reader) {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));
            if (data.content) {
              fullResponse += data.content;
              onChunk?.(data.content);
            }
            if (data.conversation_id) {
              this.conversationId = data.conversation_id;
            }
            if (data.done) {
              return {
                response: fullResponse,
                conversationId: this.conversationId || '',
              };
            }
          }
        }
      }
    }

    return { response: fullResponse, conversationId: this.conversationId || '' };
  }

  async getConversation(conversationId?: string): Promise<any> {
    const convId = conversationId || this.conversationId;
    if (!convId) {
      throw new Error('No conversation ID provided');
    }

    const headers: HeadersInit = {};
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(`${this.apiUrl}/api/conversations/${convId}`, {
      headers,
    });

    return response.json();
  }
}

// Usage
const client = new MentalCoachClient(
  'https://your-api-domain.vercel.app',
  'your-api-key'
);

const result = await client.chat("I need help", (chunk) => {
  console.log('Chunk:', chunk);
});

console.log('Full response:', result.response);
```

---

## 🎯 Platform-Specific Integrations

### Discord Bot

```python
import discord
from discord.ext import commands
import requests

bot = commands.Bot(command_prefix='!')
CHATBOT_API = "https://your-api-domain.vercel.app/api/webhook"
API_KEY = "your-api-key"

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!coach'):
        user_message = message.content[7:].strip()
        conversation_id = f"discord-{message.author.id}"
        
        response = requests.post(
            CHATBOT_API,
            json={
                "message": user_message,
                "conversation_id": conversation_id
            },
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        
        bot_response = response.json()['response']
        await message.channel.send(bot_response)
    
    await bot.process_commands(message)

bot.run('YOUR_DISCORD_TOKEN')
```

### WhatsApp Integration (using Twilio)

```python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)
CHATBOT_API = "https://your-api-domain.vercel.app/api/webhook"
API_KEY = "your-api-key"

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_message = request.values.get('Body', '')
    sender = request.values.get('From', '')
    conversation_id = f"whatsapp-{sender}"
    
    # Call chatbot API
    response = requests.post(
        CHATBOT_API,
        json={
            "message": incoming_message,
            "conversation_id": conversation_id
        },
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    bot_response = response.json()['response']
    
    resp = MessagingResponse()
    resp.message(bot_response)
    return str(resp)
```

### Telegram Bot

```python
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import requests

CHATBOT_API = "https://your-api-domain.vercel.app/api/webhook"
API_KEY = "your-api-key"

async def handle_message(update: Update, context):
    user_message = update.message.text
    user_id = update.effective_user.id
    conversation_id = f"telegram-{user_id}"
    
    response = requests.post(
        CHATBOT_API,
        json={
            "message": user_message,
            "conversation_id": conversation_id
        },
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    bot_response = response.json()['response']
    await update.message.reply_text(bot_response)

app = Application.builder().token("YOUR_TELEGRAM_TOKEN").build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
```

---

## 🔐 Authentication

### Setting Up API Key Authentication

1. Set the `API_KEY` environment variable in your backend:
```bash
export API_KEY=your-secure-api-key-here
```

2. Include the API key in requests:
```bash
curl -H "Authorization: Bearer your-secure-api-key-here" \
  https://your-api-domain.vercel.app/api/chat
```

### Disabling Authentication

If you want to disable authentication (not recommended for production), simply don't set the `API_KEY` environment variable.

---

## 📊 Health Check

Monitor your API health:

```bash
curl https://your-api-domain.vercel.app/api/health
```

Response:
```json
{
  "status": "ok",
  "version": "2.0.0",
  "database": "connected",
  "openai_configured": true
}
```

---

## 🚀 Best Practices

1. **Conversation Management**: Always use `conversation_id` to maintain context across multiple messages
2. **Error Handling**: Implement retry logic for network failures
3. **Rate Limiting**: Implement client-side rate limiting to avoid overwhelming the API
4. **Security**: Always use HTTPS in production and protect your API keys
5. **Monitoring**: Regularly check the `/api/health` endpoint

---

## 📝 Need Help?

- Check the API documentation at `/docs` (Swagger UI)
- Review error responses for troubleshooting
- Ensure your API key is correctly configured

---

**Happy Integrating! 🎉**
