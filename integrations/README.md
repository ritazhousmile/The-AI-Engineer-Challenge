# 🔌 Integration Examples

This directory contains ready-to-use integration examples for the Mental Coach AI chatbot.

## 📦 Available Integrations

### 🤖 Slack Bot
A complete Slack bot integration that allows team members to interact with the Mental Coach AI directly in Slack.

**Files:**
- `slack_bot.py` - Main bot implementation
- `slack_setup.md` - Detailed setup instructions
- `requirements.txt` - Python dependencies

**Quick Start:**
```bash
cd integrations
pip install -r requirements.txt
# Set up environment variables (see slack_setup.md)
python slack_bot.py
```

**Features:**
- Direct message support
- Channel mentions
- Slash commands (`/coach`)
- Conversation context per user
- Error handling and logging

### 🎮 Discord Bot
A Discord bot integration for communities and servers.

**Files:**
- `discord_bot.py` - Main bot implementation
- `discord_setup.md` - Detailed setup instructions

**Quick Start:**
```bash
cd integrations
pip install -r requirements.txt
# Set up environment variables (see discord_setup.md)
python discord_bot.py
```

**Features:**
- Command-based interactions (`!coach chat`)
- Direct message support
- Conversation context per user
- Error handling and logging

### 🎨 React Embeddable Widget
A beautiful, customizable React widget for embedding in websites.

**Files:**
- `react_widget/src/Widget.jsx` - React component
- `react_widget/src/Widget.css` - Styling
- `react_widget/README.md` - Integration guide

**Quick Start:**
```bash
cd integrations/react_widget
npm install
npm run build
```

**Features:**
- Modern, responsive UI
- Customizable colors and position
- Real-time streaming
- Mobile-friendly
- Easy to embed

## 🚀 Coming Soon

More integration examples:
- WhatsApp integration (Twilio)
- Telegram bot
- Microsoft Teams bot
- Email integration

## 📚 Documentation

For general integration guidance, see:
- [Integration Guide](../INTEGRATION_GUIDE.md) - Comprehensive integration documentation
- [Improvements](../IMPROVEMENTS.md) - Feature overview and improvements

## 🔧 Requirements

All integrations require:
- Python 3.8+ (for Python-based integrations)
- Access to your deployed Mental Coach AI API
- Platform-specific API keys/tokens (see individual setup guides)

## 📝 Contributing

Want to add an integration example? Feel free to:
1. Create a new integration file
2. Add setup documentation
3. Update this README
4. Submit a pull request!

---

**Happy Integrating! 🎉**
