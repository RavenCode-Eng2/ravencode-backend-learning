from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings.
    """
    # Database settings
    MONGODB_URL: str = "mongodb://localhost:27017"  # Default MongoDB URL
    DATABASE_NAME: str = "RavenCodeLearning"  # Default database name

    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"  # Default secret key
    ALGORITHM: str = "HS256"  # Default algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Default expiration time

    # Port settings for FastAPI
    API_PORT: int = 8002  # Default port is 8002

    class Config:
        env_file = ".env"  # Specify the .env file
        case_sensitive = True  # Case-sensitive configuration

# Instantiate the settings
settings = Settings()
