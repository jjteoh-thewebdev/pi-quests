from fastapi import HTTPException, Header
from app.config import settings

def verify_api_key(x_api_key: str = Header(...)):
    """
    Validate the API key in request headers.
    
    Args:
        x_api_key: API key from request header
    
    Returns:
        The validated API key
    
    Raises:
        HTTPException: If API key is invalid
    """
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "API key required"}
        )
    return x_api_key