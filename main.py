from fastapi import FastAPI, Request
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# DB credentials from Railway
DATABASE_URL = os.getenv("DATABASE_URL")

@app.post("/twilio/sms-status")
async def sms_status(request: Request):
    form = await request.form()
    sid = form.get("MessageSid")
    status = form.get("MessageStatus")
    to_number = form.get("To")
    error_code = form.get("ErrorCode")

    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        INSERT INTO sms_status (sid, status, to_number, error_code)
        VALUES ($1, $2, $3, $4)
    """, sid, status, to_number, error_code)
    await conn.close()

    return {"received": True}
