import threading
import time
import logging
from typing import Tuple, Optional


from app.libs.pi_calculator import PiCalculator
from app.repositories.redis_repository import RedisRepository
from app.config import settings

logger = logging.getLogger(__name__)

class PiService:
    """Service for managing Pi calculations and retrieval."""
    
    def __init__(self, pi_calculator: PiCalculator, repository: RedisRepository):
        """
        Initialize PiService.
        
        Args:
            pi_calculator: The Pi calculator instance
            repository: The repository for caching Pi values
        """
        self._pi_calculator = pi_calculator
        self._repository = repository
        self._is_calculating = False
        self._max_decimal_places = settings.MAX_DECIMAL_POINTS
        self._calculation_thread = None
    
    def start_calculation(self):
        """Start background calculation of Pi with increasing precision."""
        if self._is_calculating:
            return
        
        self._is_calculating = True
        self._calculation_thread = threading.Thread(
            target=self._calculate_with_increasing_precision,
            daemon=True
        )
        self._calculation_thread.start()
        logger.info("Started Pi calculation background thread")
    
    def _calculate_with_increasing_precision(self):
        """Calculate Pi with increasing precision up to max decimal places."""
        try:
            # Start with a minimal precision if nothing is cached
            cached_dp = self._repository.get_decimal_places()
            # Handle None value properly to avoid comparison error
            if cached_dp is None:
                current_dp = max(settings.START_DECIMAL_POINTS, 1)
            else:
                current_dp = max(settings.START_DECIMAL_POINTS, cached_dp)
            
            # Cache initial value if not already cached
            if current_dp == 1:
                pi_value = self._pi_calculator.calculate_pi(current_dp)
                self._repository.cache_pi(pi_value, current_dp)
            
            while current_dp < self._max_decimal_places and self._is_calculating:
                
                next_dp = current_dp + 1

                logger.info(f"Calculating Pi to {next_dp} decimal places...")
                start_time = time.time()
                
                # Calculate and cache the new value
                pi_value = self._pi_calculator.calculate_pi(next_dp)
                self._repository.cache_pi(pi_value, next_dp)

                # FOR DEBUGGING, validate accuracy
                # is_accurate = self._pi_calculator.verify_accuracy(pi_value, next_dp)
                # if not is_accurate:
                #     logger.error(f"Not Match")
                # else:
                #     logger.info(f"Match!!!!")
                
                duration = time.time() - start_time
                logger.info(f"Calculated Pi to {next_dp} decimal places in {duration:.2f} seconds")
                
                current_dp = next_dp
                
                # Slow down calculations to avoid Redis overload
                # time.sleep(0.1)
        except Exception as e:
            logger.error(f"Error in Pi calculation thread: {str(e)}")
            self._is_calculating = False
    
    def get_current_pi(self) -> Tuple[Optional[str], Optional[int]]:
        """
        Get the current cached Pi value.
        
        Returns:
            Tuple of (pi_value, decimal_places) or (None, None) if not found
        """
        return self._repository.get_cached_pi()
    
    def stop_calculation(self):
        """Stop the background calculation thread gracefully."""
        self._is_calculating = False
        if self._calculation_thread and self._calculation_thread.is_alive():
            self._calculation_thread.join(timeout=2.0)
            logger.info("Stopped Pi calculation background thread") 