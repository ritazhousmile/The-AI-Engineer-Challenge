# 🚀 Slack Bot Quick Start

Get your Slack bot running in 5 minutes!

## Prerequisites Checklist

- [ ] Slack workspace with admin access
- [ ] Mental Coach AI API deployed and accessible
- [ ] Python 3.8+ installed

## Quick Setup

### 1. Install Dependencies

```bash
cd integrations
pip install -r requirements.txt
```

### 2. Create Slack App (5 minutes)

1. Go to https://api.slack.com/apps → **Create New App**
2. **OAuth & Permissions** → Add scopes:
   - `app_mentions:read`
   - `chat:write`
   - `im:write`
   - `im:read`
   - `commands`
3. **Install to Workspace** → Copy Bot Token (`xoxb-...`)
4. **Basic Information** → Copy Signing Secret
5. **Event Subscriptions** → Enable, set URL (use ngrok for local: `https://your-ngrok-url.ngrok.io/slack/events`)
6. Subscribe to events: `app_mentions`, `message.im`
7. **Slash Commands** → Create `/coach` command

### 3. Configure Environment

Create `integrations/.env`:

```bash
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_SIGNING_SECRET=your-secret-here
CHATBOT_API_URL=https://your-api.vercel.app
CHATBOT_API_KEY=your-key-if-set
PORT=3000
```

### 4. Run Locally (with ngrok)

Terminal 1:
```bash
python slack_bot.py
```

Terminal 2:
```bash
ngrok http 3000
```

Copy ngrok URL to Slack app's Request URL.

### 5. Test It!

- DM the bot: "Hello!"
- Use command: `/coach I need help`
- Mention in channel: `@YourBotName help me`

## 🚀 Deploy to Production

### Heroku

```bash
heroku create your-slack-bot
heroku config:set SLACK_BOT_TOKEN=your-token
heroku config:set SLACK_SIGNING_SECRET=your-secret
heroku config:set CHATBOT_API_URL=your-api-url
git push heroku main
```

### Railway

1. Connect GitHub repo
2. Set environment variables
3. Deploy!

## 📚 Full Documentation

See [slack_setup.md](slack_setup.md) for detailed instructions.

## 🐛 Troubleshooting

**Bot not responding?**
- Check Request URL is correct
- Verify bot is installed in workspace
- Check logs: `python slack_bot.py`

**"Invalid signature"?**
- Verify `SLACK_SIGNING_SECRET` is correct
- Check server time is synchronized

**API errors?**
- Test API: `curl https://your-api.com/api/health`
- Verify `CHATBOT_API_URL` is correct

---

**Need help?** Check [slack_setup.md](slack_setup.md) for detailed troubleshooting.
