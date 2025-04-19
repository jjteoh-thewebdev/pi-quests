import redis
from typing import Optional, Tuple
# import asyncio
import logging

logger = logging.getLogger(__name__)

class RedisRepository:
    """Repository for caching and retrieving Pi values using Redis."""
    
    def __init__(self, redis_url: str):
        """
        Initialize Redis repository.
        
        Args:
            redis_url: Redis connection URL
        """
        self._redis = redis.from_url(redis_url)
        self._pi_key = "pi_value"
        self._dp_key = "pi_decimal_places"
    
    def is_connected(self) -> bool:
        """Check if Redis connection is established."""
        try:
            return self._redis.ping()
        except:
            return False
    
    def cache_pi(self, pi_value: str, decimal_places: int) -> bool:
        """
        Cache Pi value and decimal places in Redis.
        
        Args:
            pi_value: The calculated Pi value
            decimal_places: Number of decimal places
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a pipeline to ensure atomic operation
            pipe = self._redis.pipeline()
            pipe.set(self._pi_key, pi_value)
            pipe.set(self._dp_key, str(decimal_places))
            pipe.execute()
            logger.info(f"Cached Pi with {decimal_places} decimal places")
            return True
        except Exception as e:
            logger.error(f"Error caching Pi: {str(e)}")
            return False
    
    def get_cached_pi(self) -> Tuple[Optional[str], Optional[int]]:
        """
        Get the cached Pi value and decimal places.
        
        Returns:
            Tuple of (pi_value, decimal_places) or (None, None) if not found
        """
        try:
            # Create a pipeline to ensure atomic operation
            pipe = self._redis.pipeline()
            pipe.get(self._pi_key)
            pipe.get(self._dp_key)
            result = pipe.execute()
            
            pi_value = result[0]
            decimal_places_str = result[1]
            
            if pi_value is None or decimal_places_str is None:
                return None, None
            
            # Convert bytes to string if necessary
            if isinstance(pi_value, bytes):
                pi_value = pi_value.decode('utf-8')
            if isinstance(decimal_places_str, bytes):
                decimal_places_str = decimal_places_str.decode('utf-8')
                
            return pi_value, int(decimal_places_str)
        except Exception as e:
            logger.error(f"Error retrieving cached Pi: {str(e)}")
            return None, None
    
    def get_decimal_places(self) -> Optional[int]:
        """
        Get the current cached decimal places.
        
        Returns:
            Number of decimal places or None if not found
        """
        try:
            dp_str = self._redis.get(self._dp_key)
            if dp_str is None:
                return None
            
            if isinstance(dp_str, bytes):
                dp_str = dp_str.decode('utf-8')
                
            return int(dp_str)
        except Exception as e:
            logger.error(f"Error retrieving decimal places: {str(e)}")
            return None 