from fastapi import FastAPI, HTTPException, Header, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import json
import sqlite3
import uuid
from datetime import datetime, timedelta
from typing import Optional, List
from dotenv import load_dotenv
import logging
from contextlib import contextmanager
from collections import defaultdict
from time import time

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mental Coach AI API",
    description="A supportive AI-powered mental coach chatbot with conversation history and integrations",
    version="2.0.0"
)

# CORS configuration - can be restricted to specific origins
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if "*" not in allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# API Key authentication (optional, can be disabled)
API_KEY = os.getenv("API_KEY")  # Set this for API authentication
security = HTTPBearer(auto_error=False)

# Rate limiting configuration
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))  # requests per window
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds

# Simple in-memory rate limiter (use Redis in production)
rate_limit_store = defaultdict(list)

def check_rate_limit(request: Request):
    """Check if request is within rate limit"""
    if not RATE_LIMIT_ENABLED:
        return True
    
    client_id = request.client.host if request.client else "unknown"
    now = time()
    
    # Clean old entries
    rate_limit_store[client_id] = [
        timestamp for timestamp in rate_limit_store[client_id]
        if now - timestamp < RATE_LIMIT_WINDOW
    ]
    
    # Check limit
    if len(rate_limit_store[client_id]) >= RATE_LIMIT_REQUESTS:
        return False
    
    # Add current request
    rate_limit_store[client_id].append(now)
    return True

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for better error responses"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else "An unexpected error occurred"
        }
    )

# Database setup
DB_PATH = os.getenv("DB_PATH", "conversations.db")

def init_db():
    """Initialize the SQLite database for conversation storage"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_conversation_id ON messages(conversation_id)
    """)
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

# Initialize database on startup
init_db()

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# Request/Response Models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for maintaining context")
    system_prompt: Optional[str] = Field(None, description="Optional custom system prompt")

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    timestamp: str

class ConversationResponse(BaseModel):
    conversation_id: str
    messages: List[dict]
    created_at: str
    updated_at: str

class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    openai_configured: bool

# Authentication dependency (optional)
async def verify_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Verify API key if authentication is enabled"""
    if API_KEY:
        if not credentials or credentials.credentials != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True

@app.get("/")
def root():
    """Root endpoint to verify API is running"""
    return {
        "status": "ok",
        "message": "Mental Coach API is running!",
        "version": "2.0.0",
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat",
            "conversations": "/api/conversations",
            "webhook": "/api/webhook"
        }
    }

@app.get("/api/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint with system status"""
    db_status = "connected"
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"
        logger.error(f"Database health check failed: {e}")
    
    return HealthResponse(
        status="ok",
        version="2.0.0",
        database=db_status,
        openai_configured=bool(client and os.getenv("OPENAI_API_KEY"))
    )

@app.post("/api/chat")
async def chat(
    chat_request: ChatRequest,
    http_request: Request,
    _: bool = Depends(verify_api_key)
):
    """
    Stream chat responses from OpenAI API with Server-Sent Events.
    Supports conversation history for context-aware responses.
    """
    # Rate limiting check
    if not check_rate_limit(http_request):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds."
        )
    
    if not client or not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OPENAI_API_KEY not configured. Please set your OpenAI API key to use the chat feature."
        )
    
    # Validate message length
    if len(chat_request.message) > 5000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message too long. Maximum length is 5000 characters."
        )
    
    # Get or create conversation ID
    conversation_id = chat_request.conversation_id or str(uuid.uuid4())
    
    # System prompt
    system_prompt = chat_request.system_prompt or (
        "You are a supportive mental coach. Use markdown formatting when appropriate "
        "to make your responses clear and well-structured. Use **bold** for emphasis, "
        "bullet points for lists, and break up long responses into paragraphs."
    )
    
    # Save user message to database
    try:
        with get_db() as conn:
            # Create conversation if it doesn't exist
            conn.execute(
                "INSERT OR IGNORE INTO conversations (conversation_id) VALUES (?)",
                (conversation_id,)
            )
            # Update conversation timestamp
            conn.execute(
                "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE conversation_id = ?",
                (conversation_id,)
            )
            # Save user message
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, "user", chat_request.message)
            )
    except Exception as e:
        logger.error(f"Error saving message to database: {e}")
        # Continue even if database save fails
    
    # Log request
    logger.info(f"Chat request - Conversation: {conversation_id}, Message length: {len(chat_request.message)}")
    
    # Retrieve conversation history
    messages_history = []
    try:
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
                (conversation_id,)
            )
            messages_history = [{"role": row["role"], "content": row["content"]} for row in cursor.fetchall()]
    except Exception as e:
        logger.warning(f"Error retrieving conversation history: {e}")
    
    # Build messages for OpenAI (system + history + current user message)
    openai_messages = [{"role": "system", "content": system_prompt}]
    # Add history (excluding the last user message since we're about to add it)
    for msg in messages_history[:-1] if len(messages_history) > 1 else []:
        openai_messages.append(msg)
    # Add current user message
    openai_messages.append({"role": "user", "content": chat_request.message})
    
    async def generate():
        """Generator function that streams OpenAI responses"""
        accumulated_response = ""
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=openai_messages,
                stream=True,
                temperature=0.7
            )
            
            # Stream each chunk as it arrives
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    accumulated_response += content
                    # Send as Server-Sent Event format
                    yield f"data: {json.dumps({'content': content, 'conversation_id': conversation_id})}\n\n"
            
            # Save assistant response to database
            try:
                with get_db() as conn:
                    conn.execute(
                        "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                        (conversation_id, "assistant", accumulated_response)
                    )
                    conn.execute(
                        "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE conversation_id = ?",
                        (conversation_id,)
                    )
            except Exception as e:
                logger.error(f"Error saving assistant response: {e}")
            
            # Send done signal with conversation ID
            yield f"data: {json.dumps({'done': True, 'conversation_id': conversation_id})}\n\n"
            
        except Exception as e:
            error_message = f"Error calling OpenAI API: {str(e)}"
            logger.error(f"OpenAI API error: {e}", exc_info=True)
            # Provide user-friendly error messages
            if "rate limit" in str(e).lower():
                error_message = "API rate limit exceeded. Please try again later."
            elif "invalid" in str(e).lower() or "authentication" in str(e).lower():
                error_message = "API authentication error. Please check your configuration."
            yield f"data: {json.dumps({'error': error_message, 'conversation_id': conversation_id})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "X-Conversation-ID": conversation_id
        }
    )

@app.get("/api/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str, _: bool = Depends(verify_api_key)):
    """Retrieve a conversation by ID"""
    try:
        with get_db() as conn:
            # Get conversation metadata
            conv_cursor = conn.execute(
                "SELECT created_at, updated_at FROM conversations WHERE conversation_id = ?",
                (conversation_id,)
            )
            conv_row = conv_cursor.fetchone()
            
            if not conv_row:
                raise HTTPException(status_code=404, detail="Conversation not found")
            
            # Get messages
            msg_cursor = conn.execute(
                "SELECT role, content, timestamp FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
                (conversation_id,)
            )
            messages = [
                {
                    "role": row["role"],
                    "content": row["content"],
                    "timestamp": row["timestamp"]
                }
                for row in msg_cursor.fetchall()
            ]
            
            return ConversationResponse(
                conversation_id=conversation_id,
                messages=messages,
                created_at=conv_row["created_at"],
                updated_at=conv_row["updated_at"]
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, _: bool = Depends(verify_api_key)):
    """Delete a conversation and all its messages"""
    try:
        with get_db() as conn:
            conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            conn.execute("DELETE FROM conversations WHERE conversation_id = ?", (conversation_id,))
            return {"status": "deleted", "conversation_id": conversation_id}
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

@app.post("/api/webhook")
async def webhook_integration(
    message: str = Field(..., description="Message from external system"),
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID"),
    webhook_url: Optional[str] = Field(None, description="URL to send response to"),
    _: bool = Depends(verify_api_key)
):
    """
    Webhook endpoint for integrating with external systems.
    Accepts a message and optionally sends response to a webhook URL.
    """
    if not client or not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    
    conversation_id = conversation_id or str(uuid.uuid4())
    
    try:
        # Get conversation history if conversation_id exists
        messages_history = []
        try:
            with get_db() as conn:
                cursor = conn.execute(
                    "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
                    (conversation_id,)
                )
                messages_history = [{"role": row["role"], "content": row["content"]} for row in cursor.fetchall()]
        except Exception:
            pass
        
        # Build messages
        openai_messages = [
            {"role": "system", "content": "You are a supportive mental coach. Provide helpful, concise responses."},
            *messages_history,
            {"role": "user", "content": message}
        ]
        
        # Get response from OpenAI (non-streaming for webhooks)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=openai_messages,
            temperature=0.7
        )
        
        assistant_response = response.choices[0].message.content
        
        # Save to database
        try:
            with get_db() as conn:
                conn.execute(
                    "INSERT OR IGNORE INTO conversations (conversation_id) VALUES (?)",
                    (conversation_id,)
                )
                conn.execute(
                    "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                    (conversation_id, "user", message)
                )
                conn.execute(
                    "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                    (conversation_id, "assistant", assistant_response)
                )
        except Exception as e:
            logger.error(f"Error saving webhook conversation: {e}")
        
        # If webhook_url provided, send response there (async in production)
        if webhook_url:
            # In production, use background tasks for this
            logger.info(f"Webhook response would be sent to: {webhook_url}")
        
        return {
            "conversation_id": conversation_id,
            "response": assistant_response,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")
