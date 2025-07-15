from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()


def get_admin_token():
    """
    Get the admin token from environment variables.
    
    Returns:
        str: Admin API token
    """
    return os.getenv("ADMIN_API_TOKEN")


def validate_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Validate the admin token from the request.
    
    Args:
        credentials: The authorization credentials from the request
        
    Returns:
        str: The validated token
        
    Raises:
        HTTPException: If the token is invalid
    """
    token = credentials.credentials
    admin_token = get_admin_token()

    if not admin_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin token not configured"
        )

    if token != admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or insufficient permissions",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return token
