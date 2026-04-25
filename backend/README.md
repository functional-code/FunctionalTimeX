# FunctionalARIA Backend

Modular FastAPI backend for proactive planning, memory recall, and schedule orchestration.

## Modules

- `app/api`: HTTP routers.
- `app/models`: SQLAlchemy entities for tasks and events.
- `app/schemas`: Pydantic request and response contracts.
- `app/services`: Assistant intelligence, vector memory, calendar and messaging integrations.
- `app/db`: engine and session management.
- `app/core`: runtime config.

## Environment Setup

Copy `.env.example` to `.env` and set keys:

- `OPENAI_API_KEY` for OpenAI structured parsing.
- `GEMINI_API_KEY` for Gemini structured parsing fallback.
- `GOOGLE_CALENDAR_CREDENTIALS_JSON` for Google Calendar read access.
- `TWILIO_*` fields for WhatsApp alerts.

## Run

```bash
uvicorn app.main:app --reload
```
