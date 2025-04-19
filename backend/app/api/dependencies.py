from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings
from app.libs.pi_calculator import PiCalculator
from app.repositories.redis_repository import RedisRepository
from app.services.pi_service import PiService


# Singleton instances and their getters
limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.RATE_LIMIT_CALLS}/{settings.RATE_LIMIT_PERIOD}"])

redis_repository = RedisRepository(settings.REDIS_URL)
def get_redis_repository():
    """Get the Redis repository instance."""
    return redis_repository

pi_calculator = PiCalculator()
def get_pi_calculator():
    """Get the Pi calculator instance."""
    return pi_calculator


pi_service = PiService(get_pi_calculator(), get_redis_repository())
def get_pi_service():
    """
    Get the Pi service instance.
    
    Returns:
        PiService instance
    """
    return pi_service 