from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Helper class that initializes settings from environment variables."""
    
    # API configuration
    API_KEY: str
    
    # max dp for Pi calculation(caveat: prevent my machine from running out of memory) 
    MAX_DECIMAL_POINTS: int = 10000

    START_DECIMAL_POINTS: int = 0
    
    # Redis connection string
    REDIS_URL: str
    
    # Rate limiting configuration
    RATE_LIMIT_CALLS: int = 10
    RATE_LIMIT_PERIOD: str = "seconds"  # seconds
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings() 