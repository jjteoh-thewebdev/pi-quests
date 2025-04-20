from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.auth_guard import verify_api_key
from app.api.dependencies import get_pi_service
from app.services.pi_service import PiService

class PiResponse(BaseModel):
    """Response model for the Pi value and decimal places."""
    pi: str
    dp: str


router = APIRouter(prefix="/api", dependencies=[Depends(verify_api_key)])

@router.get("/pi", response_model=PiResponse)
async def get_pi(pi_service: PiService = Depends(get_pi_service)):
    """
    Get the current Pi value with its decimal places.
    
    Args:
        pi_service: Pi service instance
    
    Returns:
        PiResponse which containing Pi value and decimal places
    
    Raises:
        HTTPException: If Pi value is not available
    """
    pi_value, decimal_places = pi_service.get_current_pi()
    
    if pi_value is None or decimal_places is None:
        raise HTTPException(
            status_code=503,
            detail="Pi value not available. Calculation in progress."
        )
    
    return PiResponse(pi=pi_value, dp=str(decimal_places)) 