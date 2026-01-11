import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Notification(BaseModel):
    message: str

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Validate that required env vars are set
if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/send")
async def send_notification(notif: Notification):
    if not notif.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": notif.message}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload)
            # httpx doesn't automatically raise exceptions for error status codes. 
            # It only raises RequestError for network failures.
            resp.raise_for_status() # Raises HTTPStatusError if status >= 400
            
        return {"status": "sent", "message": notif.message}
    
    except httpx.HTTPStatusError as e:
        # Pass through Telegram's actual status code
        raise HTTPException(
            status_code=e.response.status_code, 
            detail=f"Telegram API error: {e.response.text}"
        )
    except httpx.RequestError as e:
        # Network/connection error - no HTTP status from Telegram
        raise HTTPException(
            status_code=502,  # Bad Gateway is semantically better
            detail=f"Failed to reach Telegram API: {str(e)}"
        )

## Key improvements:
"""
1. **Startup validation** - Fails fast if env vars are missing
2. **Timeout** - Prevents hanging requests
3. **Empty message check** - Validates input
4. **Better error handling** - Distinguishes between API errors and network issues
5. **Response includes message** - Useful for confirmation
"""
