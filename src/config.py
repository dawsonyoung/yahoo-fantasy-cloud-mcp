from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    yahoo_client_id: str
    yahoo_client_secret: str
    yahoo_league_id: str
    gcp_project_id: str | None = None
    yahoo_secret_name: str = "YAHOO_OAUTH_TOKEN"
    port: int = 8080

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
