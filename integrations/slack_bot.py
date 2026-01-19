"""
Slack Bot Integration for Mental Coach AI

This bot integrates the Mental Coach AI chatbot with Slack, allowing team members
to interact with the AI coach directly in Slack channels or DMs.

Setup:
1. Create a Slack App at https://api.slack.com/apps
2. Install the app to your workspace
3. Set up OAuth & Permissions (scopes: chat:write, im:write, app_mentions:read)
4. Get your Bot Token (starts with xoxb-)
5. Set environment variables and run this script

Usage:
    python slack_bot.py
"""

import os
import logging
import requests
from flask import Flask, request, jsonify
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
CHATBOT_API_URL = os.getenv("CHATBOT_API_URL", "http://localhost:8000")
CHATBOT_API_KEY = os.getenv("CHATBOT_API_KEY")  # Optional

# Validate configuration
if not SLACK_BOT_TOKEN:
    raise ValueError("SLACK_BOT_TOKEN environment variable is required")
if not SLACK_SIGNING_SECRET:
    raise ValueError("SLACK_SIGNING_SECRET environment variable is required")

# Initialize Slack app
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

# Initialize Flask app for handling Slack events
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


def call_chatbot_api(message: str, user_id: str, conversation_id: str = None) -> str:
    """
    Call the Mental Coach AI API to get a response.
    
    Args:
        message: User's message
        user_id: Slack user ID for conversation tracking
        conversation_id: Optional conversation ID for context
    
    Returns:
        AI assistant's response
    """
    if not conversation_id:
        conversation_id = f"slack-{user_id}"
    
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


@app.event("app_mention")
def handle_mentions(event, say):
    """
    Handle when the bot is mentioned in a channel.
    Responds in the same channel.
    """
    user_id = event.get("user")
    text = event.get("text", "")
    channel = event.get("channel")
    
    # Get bot user ID
    try:
        bot_user_id = app.client.auth_test()["user_id"]
    except Exception:
        # Fallback: try to extract from event
        bot_user_id = None
    
    # Remove the mention from the message
    if bot_user_id:
        message = text.replace(f"<@{bot_user_id}>", "").strip()
    else:
        # Fallback: remove any mention pattern
        import re
        message = re.sub(r"<@[A-Z0-9]+>", "", text).strip()
    
    if not message:
        say("Hi! I'm here to help. What's on your mind?")
        return
    
    # Get response from chatbot
    response = call_chatbot_api(message, user_id)
    
    # Send response in thread
    say(response, thread_ts=event.get("ts"))


@app.message("")
def handle_direct_messages(message, say):
    """
    Handle direct messages to the bot.
    Only responds to DMs, not channel messages (unless mentioned).
    """
    channel_type = message.get("channel_type")
    
    # Only respond to direct messages
    if channel_type != "im":
        return
    
    user_id = message.get("user")
    text = message.get("text", "").strip()
    
    if not text:
        return
    
    # Show typing indicator
    app.client.conversations_mark(channel=message.get("channel"))
    
    # Get response from chatbot
    response = call_chatbot_api(text, user_id)
    
    # Send response
    say(response)


@app.command("/coach")
def handle_coach_command(ack, respond, command):
    """
    Handle /coach slash command.
    Usage: /coach I need help with stress
    """
    ack()  # Acknowledge command immediately
    
    user_id = command.get("user_id")
    text = command.get("text", "").strip()
    
    if not text:
        respond("Please provide a message. Usage: `/coach I need help with stress`")
        return
    
    # Get response from chatbot
    response = call_chatbot_api(text, user_id)
    
    # Send response
    respond(response)


@app.event("message")
def handle_message_events(body, logger):
    """
    Handle all message events (for logging/debugging).
    """
    logger.info(f"Message event received: {body}")


# Flask routes for Slack event subscription
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """Handle Slack event subscriptions"""
    return handler.handle(request)


@flask_app.route("/slack/install", methods=["GET"])
def install():
    """OAuth installation endpoint"""
    return handler.handle(request)


@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
    """OAuth redirect handler"""
    return handler.handle(request)


@flask_app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "slack-bot",
        "chatbot_api": CHATBOT_API_URL
    })


if __name__ == "__main__":
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
    
    # Start Flask server
    port = int(os.getenv("PORT", 3000))
    logger.info(f"🚀 Starting Slack bot on port {port}")
    logger.info(f"📡 Chatbot API: {CHATBOT_API_URL}")
    flask_app.run(host="0.0.0.0", port=port, debug=False)
