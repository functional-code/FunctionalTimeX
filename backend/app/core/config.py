from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FunctionalARIA API"
    environment: str = "dev"
    database_url: str = "sqlite:///./data/functional_aria.db"
    chroma_path: str = "./chroma_store"

    openai_api_key: str = ""
    gemini_api_key: str = ""
    google_calendar_credentials_json: str = ""
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_from: str = "whatsapp:+14155238886"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
