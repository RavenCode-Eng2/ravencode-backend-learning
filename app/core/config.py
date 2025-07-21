from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings.
    """
    # Database settings
    MONGODB_URL: str = "mongodb://localhost:27017"  # Default MongoDB URL
    DATABASE_NAME: str = "RavenCodeLearning"  # Default database name

    # JWT settings
    JWT_PUBLIC_KEY: str = """
    -----BEGIN PUBLIC KEY-----
    YOUR_PUBLIC_KEY_HERE
    -----END PUBLIC KEY-----
    """  # Public key from user management service
    JWT_ALGORITHM: str = "RS256"  # Must match user management service algorithm

    # User Management service settings
    USER_MANAGEMENT_SERVICE_URL: str = "http://localhost:8001"  # Default user management service URL

    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"  # Default Redis URL
    REDIS_CACHE_TTL: int = 300  # 5 minutes default TTL

    # Port settings for FastAPI
    API_PORT: int = 8002  # Default port is 8002

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instantiate the settings
settings = Settings()
