import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

# Load .env for local development outside Docker
load_dotenv()

app = FastAPI()

class Notification(BaseModel):
    message: str

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/send")
async def send_notification(notif: Notification):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": notif.message}
    
    print(url)
    print(payload)
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Telegram API error")
    
    return {"status": "sent"}