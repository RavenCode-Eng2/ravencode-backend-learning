from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..models.auth.user import User, UserCreate, Token
from ..services.auth.auth_service import AuthService
from ..core.auth import get_current_active_user

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()

@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate) -> User:
    """Register a new user."""
    # Check if user already exists
    existing_user = await auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user with hashed password
    hashed_password = auth_service.get_password_hash(user_data.password)
    user_dict = user_data.model_dump()
    user_dict.pop("password")
    user_dict["hashed_password"] = hashed_password
    
    user = User(**user_dict)
    created_user = await auth_service.create(user)
    return User.model_validate(created_user)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """Login to get access token."""
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = await auth_service.create_user_token(user)
    return Token(access_token=access_token)

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Get current user information."""
    return current_user 