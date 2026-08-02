import json
import asyncio
import base64
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from services.groq_service import groq_service
from services.weather_service import get_weather_forecast
from services.sms_service import handle_incoming_sms
from config import settings
from auth import get_optional_user

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    city: Optional[str] = None
    language: Optional[str] = None  # "fr" or "wo" or "en"
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    language: str
    agents_used: list[str]
    metadata: Optional[dict] = None


class SMSRequest(BaseModel):
    From: str
    Body: str


# --- Chat endpoint (main) ---
@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, user_id: str | None = Depends(get_optional_user)):
    try:
        response_text = await groq_service.chat(
            message=req.message,
            language=req.language or "en",
            city=req.city
        )
        return {
            "response": response_text,
            "language": req.language or "en",
            "agents_used": ["groq_chat"],
            "metadata": None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Streaming chat endpoint (SSE) ---
@router.post("/chat/stream")
async def chat_stream(req: ChatRequest, user_id: str | None = Depends(get_optional_user)):
    async def event_stream():
        try:
            yield f"data: {json.dumps({'type': 'routing', 'agents': ['groq_chat']})}\n\n"

            async for chunk in groq_service.chat_stream(
                message=req.message,
                language=req.language or "en",
                city=req.city
            ):
                yield f"data: {json.dumps({'type': 'token', 'text': chunk})}\n\n"
                # await asyncio.sleep(0.01) # Groq is fast, we can let it stream as fast as it wants

            yield f"data: {json.dumps({'type': 'done', 'agents_used': ['groq_chat'], 'language': req.language or 'en'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# --- Weather endpoint ---
@router.get("/weather/{city}")
async def weather(city: str):
    try:
        data = await get_weather_forecast(city)
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- SMS webhook ---
@router.post("/sms/incoming")
async def sms_incoming(req: SMSRequest):
    try:
        response = await handle_incoming_sms(req.From, req.Body)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Crop photo diagnosis (Groq Vision) ---
@router.post("/diagnose")
async def diagnose_crop(
    image: UploadFile = File(...),
    language: str = Form("en"),
):
    try:
        image_data = await image.read()
        b64 = base64.b64encode(image_data).decode("utf-8")

        content_type = image.content_type or "image/jpeg"
        if content_type not in ("image/jpeg", "image/png", "image/gif", "image/webp"):
            content_type = "image/jpeg"

        diagnosis_text = await groq_service.diagnose_vision(
            image_base64=b64,
            mime_type=content_type,
            language=language
        )

        return {
            "diagnosis": diagnosis_text,
            "language": language,
            "agents_used": ["groq_vision"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Data endpoints ---
@router.get("/crops")
async def list_crops():
    from data_loader import load_crops
    return load_crops()


@router.get("/markets")
async def list_markets():
    from data_loader import load_markets
    return load_markets()


@router.get("/zones")
async def list_zones():
    from data_loader import load_zones
    return load_zones()


@router.get("/cities")
async def list_cities():
    from config import settings
    return settings.CITIES
