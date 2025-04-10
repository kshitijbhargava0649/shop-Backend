from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from ..auth.controller import AuthController

class AuthMiddleware(HTTPBearer):
    def __init__(self, auth_controller: AuthController):
        super().__init__()
        self.auth_controller = auth_controller

    async def __call__(self, request: Request) -> Optional[str]:
        """Validate JWT token in request"""
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        try:
            # Validate token and get user
            user = await self.auth_controller.get_current_user(credentials.credentials)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return credentials.credentials
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            ) 