# 🤖 Discord Bot Integration Setup Guide

This guide will walk you through setting up the Mental Coach AI chatbot as a Discord bot.

## 📋 Prerequisites

- A Discord account
- A Discord server where you have admin permissions
- Python 3.8+ installed
- Your Mental Coach AI API deployed and accessible

## 🚀 Step-by-Step Setup

### Step 1: Create a Discord Application

1. Go to [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Enter a name: `Mental Coach AI` (or any name you prefer)
4. Click **"Create"**

### Step 2: Create a Bot

1. In your application, go to **"Bot"** in the left sidebar
2. Click **"Add Bot"**
3. Click **"Yes, do it!"** to confirm
4. Under **"Token"**, click **"Reset Token"** or **"Copy"**
   - **⚠️ IMPORTANT:** Save this token! You won't be able to see it again.
   - This is your `DISCORD_BOT_TOKEN`

### Step 3: Configure Bot Settings

1. Still in the **"Bot"** section, configure:
   - **Username**: Set a display name
   - **Icon**: Upload a bot avatar (optional)
   - **Public Bot**: Toggle OFF (unless you want it public)
   - **Requires OAuth2 Code Grant**: Leave OFF

2. Under **"Privileged Gateway Intents"**, enable:
   - ✅ **MESSAGE CONTENT INTENT** (Required to read message content)
   - ✅ **SERVER MEMBERS INTENT** (Optional, for member info)

### Step 4: Generate Invite URL

1. Go to **"OAuth2"** → **"URL Generator"** in the left sidebar
2. Under **"Scopes"**, select:
   - `bot`
   - `applications.commands` (optional, for slash commands)
3. Under **"Bot Permissions"**, select:
   - `Send Messages`
   - `Read Message History`
   - `Use External Emojis`
   - `Add Reactions` (optional)
4. Copy the **"Generated URL"** at the bottom
5. Open the URL in your browser
6. Select your server and click **"Authorize"**
7. Complete the CAPTCHA if prompted

### Step 5: Install Dependencies

```bash
cd integrations
pip install discord.py requests python-dotenv
```

Or update `requirements.txt`:
```txt
discord.py>=2.3.0
requests>=2.31.0
python-dotenv>=1.0.0
```

### Step 6: Configure Environment Variables

Create a `.env` file in the `integrations` directory:

```bash
# Discord Configuration
DISCORD_BOT_TOKEN=your-discord-bot-token-here

# Chatbot API Configuration
CHATBOT_API_URL=https://your-chatbot-api.vercel.app
CHATBOT_API_KEY=your-api-key-if-configured

# Optional - Bot Configuration
BOT_PREFIX=!coach
```

### Step 7: Run the Bot

```bash
python discord_bot.py
```

You should see:
```
✅ Mental Coach AI#1234 has connected to Discord!
✅ Chatbot API is accessible
```

## 🎯 Usage

### Basic Commands

**Chat with the bot:**
```
!coach chat I'm feeling stressed about work
```

**Get help:**
```
!coach help
```

**Clear conversation:**
```
!coach clear
```

**Bot info:**
```
!coach info
```

### Command Aliases

- `!coach chat` or `!coach c` - Chat with AI
- `!coach help` - Show help
- `!coach clear` or `!coach reset` - Clear history
- `!coach info` or `!coach about` or `!coach status` - Bot info

## 🔧 Configuration Options

### Custom Prefix

Change the command prefix by setting `BOT_PREFIX`:
```bash
BOT_PREFIX=!mental
```

Then commands become: `!mental chat [message]`

### Conversation Context

The bot automatically maintains conversation context per user using conversation IDs in the format: `discord-{user_id}`

## 🚀 Deployment

### Option 1: Run on Your Computer

Simply run:
```bash
python discord_bot.py
```

Keep the terminal open. The bot will stay online as long as the script is running.

### Option 2: Deploy to Cloud

#### Heroku

1. Create `Procfile`:
   ```
   worker: python discord_bot.py
   ```

2. Deploy:
   ```bash
   heroku create your-discord-bot
   heroku config:set DISCORD_BOT_TOKEN=your-token
   heroku config:set CHATBOT_API_URL=your-api-url
   git push heroku main
   ```

#### Railway

1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically

#### DigitalOcean App Platform

1. Create new app
2. Connect GitHub repository
3. Set environment variables
4. Deploy

#### AWS/GCP/Azure

Use container services or serverless functions.

### Option 3: VPS (Virtual Private Server)

1. SSH into your VPS
2. Install Python and dependencies
3. Use `screen` or `tmux` to keep bot running:
   ```bash
   screen -S discord-bot
   python discord_bot.py
   # Press Ctrl+A then D to detach
   ```

4. Or use a process manager like `pm2`:
   ```bash
   npm install -g pm2
   pm2 start discord_bot.py --interpreter python3
   pm2 save
   pm2 startup
   ```

## 🐛 Troubleshooting

### Bot not responding

- **Check bot is online**: Look for the green dot next to bot name in Discord
- **Verify token**: Make sure `DISCORD_BOT_TOKEN` is correct
- **Check permissions**: Bot needs "Send Messages" permission
- **Check logs**: Look for error messages in console

### "MESSAGE CONTENT INTENT" errors

- Go to Discord Developer Portal → Your App → Bot
- Enable **"MESSAGE CONTENT INTENT"** under Privileged Gateway Intents
- Save changes
- Re-invite bot to server if needed

### API connection errors

- Verify `CHATBOT_API_URL` is correct
- Test API directly: `curl https://your-api.com/api/health`
- Check firewall/network settings
- Ensure API is accessible from bot's location

### Rate limiting

- Discord has rate limits (50 requests/second)
- The chatbot API also has rate limits
- If you hit limits, wait a moment and try again

### Bot goes offline

- Check if the script is still running
- Look for error messages in logs
- Verify token hasn't been reset
- Check server/VPS status if deployed

## 🔒 Security Best Practices

1. **Never share your bot token**
   - Keep it in `.env` file
   - Add `.env` to `.gitignore`
   - Never commit tokens to version control

2. **Use environment variables**
   - Store all sensitive data in environment variables
   - Use different tokens for development/production

3. **Limit bot permissions**
   - Only grant necessary permissions
   - Don't give admin permissions unless needed

4. **Monitor bot activity**
   - Check logs regularly
   - Set up alerts for errors
   - Monitor API usage

## 📊 Monitoring

The bot logs important events:
- Connection status
- Command usage
- API errors
- General errors

Check logs to monitor bot health and usage.

## 🎨 Customization

### Change Bot Status

Edit `on_ready()` function to customize bot status:
```python
await bot.change_presence(
    activity=discord.Game(name="Helping with mental wellness"),
    status=discord.Status.online
)
```

### Add More Commands

Add new commands by creating new `@bot.command()` functions:
```python
@bot.command(name="motivate")
async def motivate_command(ctx):
    response = call_chatbot_api("Give me motivation", str(ctx.author.id))
    await ctx.send(response)
```

### Custom Responses

Modify the `call_chatbot_api()` function to customize how responses are formatted or processed.

## 📚 Additional Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs/)
- [Mental Coach AI Integration Guide](../INTEGRATION_GUIDE.md)

## 🎉 Success!

Your Discord bot is now ready! Test it in your server:

```
!coach chat Hello!
```

---

**Need help?** Check the logs for error messages or review the [Integration Guide](../INTEGRATION_GUIDE.md).
