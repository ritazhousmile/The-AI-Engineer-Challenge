from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS so the frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize OpenAI client (will be None if key not set)
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    """Root endpoint to verify API is running"""
    return {
        "status": "ok",
        "message": "Mental Coach API is running!",
        "endpoints": {
            "health": "/",
            "chat": "/api/chat"
        }
    }

@app.get("/api")
def api_root():
    """API root endpoint"""
    return {
        "status": "ok",
        "message": "Mental Coach API",
        "version": "1.0.0"
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Stream chat responses from OpenAI API with Server-Sent Events"""
    if not client or not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured. Please set your OpenAI API key to use the chat feature.")
    
    async def generate():
        """Generator function that streams OpenAI responses"""
        try:
            user_message = request.message
            stream = client.chat.completions.create(
                model="gpt-4o-mini",  # Using gpt-4o-mini for better reliability
                messages=[
                    {"role": "system", "content": "You are a supportive mental coach. Use markdown formatting when appropriate to make your responses clear and well-structured. Use **bold** for emphasis, bullet points for lists, and break up long responses into paragraphs."},
                    {"role": "user", "content": user_message}
                ],
                stream=True
            )
            
            # Stream each chunk as it arrives
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    # Send as Server-Sent Event format
                    yield f"data: {json.dumps({'content': content})}\n\n"
            
            # Send done signal
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            error_message = f"Error calling OpenAI API: {str(e)}"
            yield f"data: {json.dumps({'error': error_message})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
