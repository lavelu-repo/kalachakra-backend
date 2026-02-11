"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_RELOAD: bool = True
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]


    EPHEMERIS_PATH: str = "./ephe"
    ZODIAC_TYPE: str = "tropical" # tropical | sidereal
    AYANAMSA: str = "LAHIRI" # LAHIRI | RAMAN | KRISHNAMURTI
    USE_TRUE_NODE: bool = True # True | False


settings = AppConfig()