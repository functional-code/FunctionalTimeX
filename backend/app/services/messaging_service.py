from app.core.config import settings

try:
    from twilio.rest import Client
except ImportError:
    Client = None


class MessagingService:
    def __init__(self) -> None:
        if settings.twilio_account_sid and settings.twilio_auth_token and Client:
            self.client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        else:
            self.client = None

    def send_whatsapp_alert(self, to_number: str, message: str) -> dict:
        if not self.client:
            return {"status": "skipped", "reason": "twilio_not_configured"}

        outgoing = self.client.messages.create(
            from_=settings.twilio_whatsapp_from,
            body=message,
            to=to_number,
        )
        return {"status": "sent", "sid": outgoing.sid}
