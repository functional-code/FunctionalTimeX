import json
from datetime import datetime, timedelta, timezone

from app.core.config import settings

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
except ImportError:
    Credentials = None
    build = None


class CalendarService:
    def get_upcoming(self) -> list[dict]:
        if settings.google_calendar_credentials_json and Credentials and build:
            return self._from_google()
        return self._fallback()

    def _from_google(self) -> list[dict]:
        creds_data = json.loads(settings.google_calendar_credentials_json)
        creds = Credentials.from_service_account_info(
            creds_data, scopes=["https://www.googleapis.com/auth/calendar.readonly"]
        )
        service = build("calendar", "v3", credentials=creds)
        now = datetime.now(timezone.utc).isoformat()
        events = (
            service.events()
            .list(calendarId="primary", timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime")
            .execute()
            .get("items", [])
        )
        return [
            {
                "title": event.get("summary", "Untitled"),
                "start_at": event.get("start", {}).get("dateTime", ""),
                "end_at": event.get("end", {}).get("dateTime", ""),
                "source": "google",
                "external_id": event.get("id", ""),
            }
            for event in events
        ]

    def _fallback(self) -> list[dict]:
        now = datetime.utcnow()
        return [
            {
                "title": "Deep Work Block",
                "start_at": (now + timedelta(hours=2)).isoformat(),
                "end_at": (now + timedelta(hours=4)).isoformat(),
                "source": "local",
                "external_id": "",
            }
        ]
