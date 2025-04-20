from fastapi import HTTPException, Header
from typing import Optional
from app.config import settings

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Validate the API key in request headers.
    
    Args:
        x_api_key: API key from request header
    
    Returns:
        The validated API key
    
    Raises:
        HTTPException: If API key is invalid or missing
    """
    # Check if API key is missing
    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="API key is missing",
            headers={"WWW-Authenticate": "API key required"}
        )

    # Check if API key is invalid
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "API key required"}
        )
        
    return x_api_key