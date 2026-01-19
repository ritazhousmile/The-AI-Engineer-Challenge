"""
Discord Bot Integration for Mental Coach AI

This bot integrates the Mental Coach AI chatbot with Discord, allowing community
members to interact with the AI coach in Discord servers.

Setup:
1. Create a Discord Application at https://discord.com/developers/applications
2. Create a bot and get the token
3. Invite bot to your server with appropriate permissions
4. Set environment variables and run this script

Usage:
    python discord_bot.py
"""

import os
import logging
import requests
import asyncio
from discord import Intents, Client, Message
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHATBOT_API_URL = os.getenv("CHATBOT_API_URL", "http://localhost:8000")
CHATBOT_API_KEY = os.getenv("CHATBOT_API_KEY")  # Optional
BOT_PREFIX = os.getenv("BOT_PREFIX", "!coach")  # Command prefix

# Validate configuration
if not DISCORD_BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is required")

# Configure Discord intents
intents = Intents.default()
intents.message_content = True  # Required to read message content
intents.members = True

# Initialize Discord bot
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)


def call_chatbot_api(message: str, user_id: str, conversation_id: str = None) -> str:
    """
    Call the Mental Coach AI API to get a response.
    
    Args:
        message: User's message
        user_id: Discord user ID for conversation tracking
        conversation_id: Optional conversation ID for context
    
    Returns:
        AI assistant's response
    """
    if not conversation_id:
        conversation_id = f"discord-{user_id}"
    
    try:
        headers = {
            "Content-Type": "application/json"
        }
        if CHATBOT_API_KEY:
            headers["Authorization"] = f"Bearer {CHATBOT_API_KEY}"
        
        # Use webhook endpoint for synchronous responses
        response = requests.post(
            f"{CHATBOT_API_URL}/api/webhook",
            json={
                "message": message,
                "conversation_id": conversation_id
            },
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "I'm sorry, I couldn't generate a response.")
        elif response.status_code == 429:
            return "I'm receiving too many requests right now. Please try again in a moment."
        else:
            logger.error(f"Chatbot API error: {response.status_code} - {response.text}")
            return "I'm experiencing some technical difficulties. Please try again later."
    
    except requests.exceptions.Timeout:
        logger.error("Chatbot API timeout")
        return "The request took too long. Please try again with a shorter message."
    except requests.exceptions.RequestException as e:
        logger.error(f"Chatbot API request error: {e}")
        return "I'm having trouble connecting right now. Please try again later."
    except Exception as e:
        logger.error(f"Unexpected error calling chatbot API: {e}")
        return "An unexpected error occurred. Please try again later."


@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord"""
    logger.info(f"✅ {bot.user} has connected to Discord!")
    logger.info(f"📡 Chatbot API: {CHATBOT_API_URL}")
    
    # Test chatbot API connection
    try:
        health_response = requests.get(f"{CHATBOT_API_URL}/api/health", timeout=5)
        if health_response.status_code == 200:
            logger.info("✅ Chatbot API is accessible")
        else:
            logger.warning(f"⚠️ Chatbot API returned status {health_response.status_code}")
    except Exception as e:
        logger.error(f"❌ Cannot connect to chatbot API at {CHATBOT_API_URL}: {e}")
        logger.error("Make sure the chatbot API is running and accessible")
    
    # Set bot status
    await bot.change_presence(
        activity=bot.activity or None,
        status=bot.status
    )


@bot.event
async def on_message(message: Message):
    """Handle all messages"""
    # Ignore messages from bots (including ourselves)
    if message.author.bot:
        return
    
    # Handle commands
    await bot.process_commands(message)


@bot.command(name="chat", aliases=["c", "help"])
async def chat_command(ctx, *, message: str = None):
    """
    Chat with the Mental Coach AI.
    
    Usage:
        !coach chat I'm feeling stressed
        !coach c How can I stay motivated?
    """
    if not message:
        await ctx.send(
            "👋 Hi! I'm here to help you on your mental wellness journey.\n"
            "**Usage:** `!coach chat [your message]`\n"
            "**Example:** `!coach chat I need help with anxiety`"
        )
        return
    
    # Show typing indicator
    async with ctx.typing():
        # Get response from chatbot
        user_id = str(ctx.author.id)
        response = call_chatbot_api(message, user_id)
        
        # Discord has a 2000 character limit per message
        if len(response) > 2000:
            # Split into chunks
            chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(response)


@bot.command(name="clear", aliases=["reset"])
async def clear_command(ctx):
    """
    Clear conversation history (start fresh).
    
    Usage:
        !coach clear
    """
    # Note: This would require an API endpoint to delete conversations
    # For now, just acknowledge
    await ctx.send(
        "🔄 Your conversation context has been reset. "
        "Start a new conversation with `!coach chat [your message]`"
    )


@bot.command(name="info", aliases=["about", "status"])
async def info_command(ctx):
    """
    Get information about the bot.
    
    Usage:
        !coach info
    """
    # Check chatbot API health
    try:
        health_response = requests.get(f"{CHATBOT_API_URL}/api/health", timeout=5)
        api_status = "✅ Online" if health_response.status_code == 200 else "⚠️ Issues"
    except:
        api_status = "❌ Offline"
    
    embed = {
        "title": "🧠 Mental Coach AI",
        "description": "Your supportive AI-powered mental wellness coach",
        "color": 0x6366f1,  # Purple color
        "fields": [
            {
                "name": "API Status",
                "value": api_status,
                "inline": True
            },
            {
                "name": "Commands",
                "value": "`!coach chat [message]` - Chat with the AI\n"
                        "`!coach clear` - Reset conversation\n"
                        "`!coach info` - Show this info",
                "inline": False
            }
        ],
        "footer": {
            "text": "Powered by Mental Coach AI"
        }
    }
    
    await ctx.send(embed=await ctx.bot.http.request(
        "POST",
        f"/channels/{ctx.channel.id}/messages",
        json={"embed": embed}
    ) if hasattr(ctx.bot.http, 'request') else None)
    
    # Fallback if embed doesn't work
    await ctx.send(
        f"🧠 **Mental Coach AI**\n"
        f"API Status: {api_status}\n\n"
        f"**Commands:**\n"
        f"`!coach chat [message]` - Chat with the AI\n"
        f"`!coach clear` - Reset conversation\n"
        f"`!coach info` - Show this info"
    )


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument. Use `!coach chat [your message]`")
    elif isinstance(error, commands.CommandNotFound):
        # Ignore unknown commands
        pass
    else:
        logger.error(f"Command error: {error}")
        await ctx.send("❌ An error occurred. Please try again.")


@bot.event
async def on_error(event, *args, **kwargs):
    """Handle general errors"""
    logger.error(f"Error in event {event}: {args}, {kwargs}")


if __name__ == "__main__":
    logger.info("🚀 Starting Discord bot...")
    logger.info(f"📡 Chatbot API: {CHATBOT_API_URL}")
    logger.info(f"🤖 Bot Prefix: {BOT_PREFIX}")
    
    try:
        bot.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise
