# 🤖 Slack Bot Integration Setup Guide

This guide will walk you through setting up the Mental Coach AI chatbot as a Slack bot.

## 📋 Prerequisites

- A Slack workspace where you have permission to install apps
- Python 3.8+ installed
- Your Mental Coach AI API deployed and accessible
- A server or cloud platform to host the bot (or use ngrok for local development)

## 🚀 Step-by-Step Setup

### Step 1: Create a Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Enter app name: `Mental Coach AI` (or any name you prefer)
5. Select your workspace
6. Click **"Create App"**

### Step 2: Configure Bot Token Scopes

1. In your app settings, go to **"OAuth & Permissions"** in the left sidebar
2. Scroll down to **"Scopes"** → **"Bot Token Scopes"**
3. Add the following scopes:
   - `app_mentions:read` - Listen for mentions
   - `chat:write` - Send messages
   - `im:write` - Send direct messages
   - `im:read` - Read direct messages
   - `channels:history` - Read channel messages (if needed)
   - `commands` - Add slash commands

### Step 3: Install App to Workspace

1. Still in **"OAuth & Permissions"**, scroll to the top
2. Click **"Install to Workspace"**
3. Review permissions and click **"Allow"**
4. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)
   - This is your `SLACK_BOT_TOKEN`

### Step 4: Get Signing Secret

1. Go to **"Basic Information"** in the left sidebar
2. Under **"App Credentials"**, find **"Signing Secret"**
3. Click **"Show"** and copy it
   - This is your `SLACK_SIGNING_SECRET`

### Step 5: Configure Event Subscriptions

1. Go to **"Event Subscriptions"** in the left sidebar
2. Toggle **"Enable Events"** to ON
3. Set **Request URL** to your server URL + `/slack/events`
   - Example: `https://your-domain.com/slack/events`
   - For local development, use ngrok (see below)
4. Under **"Subscribe to bot events"**, add:
   - `app_mentions` - When bot is mentioned
   - `message.im` - Direct messages to bot
5. Click **"Save Changes"**

### Step 6: Add Slash Command (Optional)

1. Go to **"Slash Commands"** in the left sidebar
2. Click **"Create New Command"**
3. Configure:
   - **Command**: `/coach`
   - **Request URL**: `https://your-domain.com/slack/events`
   - **Short Description**: `Chat with Mental Coach AI`
   - **Usage Hint**: `[your message]`
4. Click **"Save"**

### Step 7: Install Dependencies

```bash
cd integrations
pip install slack-bolt flask requests python-dotenv
```

Or create a `requirements.txt`:

```txt
slack-bolt>=1.18.0
flask>=3.0.0
requests>=2.31.0
python-dotenv>=1.0.0
```

### Step 8: Configure Environment Variables

Create a `.env` file in the `integrations` directory:

```bash
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here

# Chatbot API Configuration
CHATBOT_API_URL=https://your-chatbot-api.vercel.app
CHATBOT_API_KEY=your-api-key-if-configured

# Server Configuration
PORT=3000
```

### Step 9: Run the Bot

```bash
python slack_bot.py
```

The bot should start and be ready to receive messages!

## 🧪 Testing Locally with ngrok

For local development, you'll need to expose your local server:

1. Install ngrok: [https://ngrok.com/download](https://ngrok.com/download)

2. Start your bot:
   ```bash
   python slack_bot.py
   ```

3. In another terminal, start ngrok:
   ```bash
   ngrok http 3000
   ```

4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

5. Update your Slack app's **Request URL** to:
   ```
   https://abc123.ngrok.io/slack/events
   ```

6. Save changes in Slack app settings

## 🎯 Usage

### Direct Messages
Users can DM the bot directly:
- User: "I'm feeling stressed about work"
- Bot: [AI response]

### Channel Mentions
Users can mention the bot in channels:
- User: "@Mental Coach AI I need help staying motivated"
- Bot: [AI response in thread]

### Slash Command
Users can use the `/coach` command:
- User: `/coach I want to build better habits`
- Bot: [AI response]

## 🔧 Configuration Options

### Conversation Context
The bot automatically maintains conversation context per user using conversation IDs in the format: `slack-{user_id}`

### Custom System Prompt
You can modify the system prompt by editing the `call_chatbot_api` function to include a custom `system_prompt` parameter.

### Rate Limiting
The chatbot API has built-in rate limiting. If you encounter rate limit errors, you can:
1. Adjust rate limits in your chatbot API configuration
2. Implement client-side rate limiting in the bot

## 🚀 Deployment

### Option 1: Deploy to Heroku

1. Create a `Procfile`:
   ```
   web: python slack_bot.py
   ```

2. Deploy:
   ```bash
   heroku create your-slack-bot
   heroku config:set SLACK_BOT_TOKEN=your-token
   heroku config:set SLACK_SIGNING_SECRET=your-secret
   heroku config:set CHATBOT_API_URL=your-api-url
   git push heroku main
   ```

### Option 2: Deploy to Railway

1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically

### Option 3: Deploy to AWS/GCP/Azure

Use your preferred cloud platform's container or serverless options.

## 🐛 Troubleshooting

### Bot not responding
- Check that the bot is installed in your workspace
- Verify the Request URL is correct and accessible
- Check bot logs for errors
- Ensure the chatbot API is running and accessible

### "Invalid signature" errors
- Verify `SLACK_SIGNING_SECRET` is correct
- Check that your server time is synchronized
- Ensure the Request URL matches exactly

### API connection errors
- Verify `CHATBOT_API_URL` is correct
- Check that the chatbot API is running
- Test the API directly: `curl https://your-api.com/api/health`

### Rate limiting
- The chatbot API has rate limits
- Consider implementing request queuing
- Monitor API usage

## 📊 Monitoring

The bot includes a health check endpoint:
```bash
curl http://localhost:3000/health
```

Response:
```json
{
  "status": "ok",
  "service": "slack-bot",
  "chatbot_api": "https://your-api.com"
}
```

## 🔒 Security Best Practices

1. **Never commit tokens to version control**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Use HTTPS in production**
   - Slack requires HTTPS for event subscriptions
   - Use a reverse proxy or cloud platform

3. **Rotate tokens regularly**
   - Update tokens if compromised
   - Use Slack's token rotation features

4. **Monitor API usage**
   - Track chatbot API calls
   - Set up alerts for unusual activity

## 📚 Additional Resources

- [Slack API Documentation](https://api.slack.com/)
- [slack-bolt Python SDK](https://slack.dev/bolt-python/)
- [Mental Coach AI Integration Guide](../INTEGRATION_GUIDE.md)

## 🎉 Success!

Once set up, your team can now interact with the Mental Coach AI directly in Slack!

**Test it out:**
1. DM the bot: "Hello!"
2. Mention it in a channel: "@Mental Coach AI I need help"
3. Use the slash command: `/coach How can I reduce stress?`

---

**Need help?** Check the [Integration Guide](../INTEGRATION_GUIDE.md) or review the bot logs for error messages.
