from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    DATABASE_URL: str = "sqlite:///./test.db"  # Bot database (metadata, users, roles, etc.)
    TRANS_DATABASE_URL: str = "sqlite:///./data.db"  # Transactional database for queries
    JWT_SECRET_KEY: str = "gMnRc4vL56geGzgrh19YtQ9W3xFz8XyD"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 3060  # 51 hours
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore'
    )

settings = Settings()