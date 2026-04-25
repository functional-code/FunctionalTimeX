import json
from datetime import datetime

from app.core.config import settings
from app.schemas.assistant import ParsedIntent

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
try:
    import google.generativeai as genai
except ImportError:
    genai = None


class LLMParser:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if OpenAI and settings.openai_api_key else None
        self.gemini_model = None
        if genai and settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    def parse(self, message: str) -> ParsedIntent:
        if not self.client:
            if self.gemini_model:
                return self._parse_with_gemini(message)
            return self._fallback(message)

        prompt = (
            "Extract intent from user message and return strict JSON with keys: "
            "intent(string), confidence(float 0-1), extracted_tasks(list[string]), "
            "suggested_event_time(ISO8601 or null), risk_level(string). "
            f"Message: {message}"
        )
        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            text={"format": {"type": "json_object"}},
        )
        raw = response.output_text
        payload = json.loads(raw)
        suggested = payload.get("suggested_event_time")
        payload["suggested_event_time"] = datetime.fromisoformat(suggested) if suggested else None
        return ParsedIntent(**payload)

    def _parse_with_gemini(self, message: str) -> ParsedIntent:
        prompt = (
            "Return ONLY strict JSON with keys: intent, confidence, extracted_tasks, suggested_event_time, risk_level. "
            f"Analyze: {message}"
        )
        response = self.gemini_model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"},
        )
        payload = json.loads(response.text)
        suggested = payload.get("suggested_event_time")
        payload["suggested_event_time"] = datetime.fromisoformat(suggested) if suggested else None
        return ParsedIntent(**payload)

    def _fallback(self, message: str) -> ParsedIntent:
        lowered = message.lower()
        intent = "plan_day" if "schedule" in lowered or "today" in lowered else "task_capture"
        tasks = [message.strip()] if intent == "task_capture" else ["Prioritize top 3 outcomes"]
        return ParsedIntent(
            intent=intent,
            confidence=0.62,
            extracted_tasks=tasks,
            suggested_event_time=None,
            risk_level="medium" if "urgent" in lowered else "low",
        )
