import groq
import json
from config import settings
import logging
from data_loader import load_markets

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        self.client = groq.AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        self.vision_model = settings.GROQ_VISION_MODEL

    async def chat_stream(self, message: str, language: str = "en", city: str = None):
        """Streams a chat response back to the client using Groq."""
        system_prompt = f"You are AgriAgent, an expert agricultural advisor. The user speaks {language}. Provide practical advice."
        if city:
            system_prompt += f" The user is located near {city}. Tailor advice to this region's climate."

        # Inject market data
        try:
            markets_data = load_markets()
            system_prompt += f"\n\nHere is the latest market price and trend data across various states/regions:\n{json.dumps(markets_data.get('prices', {}), indent=2)}"
        except Exception as e:
            logger.error(f"Failed to load market data: {e}")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
            )
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            logger.error(f"Groq chat_stream error: {e}")
            raise e

    async def chat(self, message: str, language: str = "en", city: str = None):
        """Non-streaming chat response."""
        system_prompt = f"You are AgriAgent, an expert agricultural advisor. The user speaks {language}. Provide practical advice."
        if city:
            system_prompt += f" The user is located near {city}. Tailor advice to this region's climate."

        # Inject market data
        try:
            markets_data = load_markets()
            system_prompt += f"\n\nHere is the latest market price and trend data across various states/regions:\n{json.dumps(markets_data.get('prices', {}), indent=2)}"
        except Exception as e:
            logger.error(f"Failed to load market data: {e}")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq chat error: {e}")
            raise e

    async def diagnose_vision(self, image_base64: str, mime_type: str, language: str = "en"):
        """Analyzes an image using Groq's Vision model."""
        lang_label = {"en": "English", "fr": "French", "wo": "Wolof"}.get(language, "English")
        
        system_prompt = (
            "You are an expert agricultural advisor for farmers worldwide.\n"
            "Analyze this photo of a crop/plant and provide:\n"
            "1. **Identified crop** (if recognizable)\n"
            "2. **Health assessment** - is the plant healthy or showing signs of disease/stress?\n"
            "3. **Diagnosis** - if diseased, identify the most likely disease or pest\n"
            "4. **Symptoms spotted** - describe what you see in the image\n"
            "5. **Treatment** - practical treatment steps using methods available locally (including traditional/organic methods)\n"
            "6. **Prevention** - how to prevent this in the future\n"
            "\n"
            "Be specific, practical, and context-aware (local climate, available products, etc).\n"
            "Use markdown tables for structured data when appropriate.\n"
            f"Respond in {lang_label}."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Analyze this crop photo."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_base64}"
                        },
                    },
                ],
            },
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.vision_model,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq vision error: {e}")
            raise e

groq_service = GroqService()
