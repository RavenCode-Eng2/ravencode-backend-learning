from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from .config import settings

security = HTTPBearer()

def decode_and_validate_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate the JWT using the public key.
    Returns the decoded token payload if valid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_PUBLIC_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    FastAPI dependency that validates the JWT and returns the user payload.
    """
    return decode_and_validate_token(credentials.credentials)

def require_roles(allowed_roles: list[str]):
    """
    Create a dependency that checks if the user has any of the allowed roles.
    """
    async def role_checker(
        user_payload: Dict[str, Any] = Depends(get_current_user_payload)
    ) -> Dict[str, Any]:
        user_roles = user_payload.get("roles", [])
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return user_payload
    return role_checker

# Common role-based dependencies
require_admin = require_roles(["admin"])
require_instructor = require_roles(["admin", "instructor"])
require_student = require_roles(["admin", "instructor", "student"]) 