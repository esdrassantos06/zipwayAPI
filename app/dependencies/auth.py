from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

security = HTTPBearer()

class AdminToken:
    def __init__(self):
        load_dotenv()
        self.__token = os.getenv("ADMIN_API_TOKEN")
        if not self.__token:
            raise RuntimeError("Admin token not configured")

    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        token = credentials.credentials
        if token != self.__token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or insufficient permissions",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return token