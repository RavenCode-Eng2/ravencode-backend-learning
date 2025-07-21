from datetime import datetime, timedelta
from typing import Optional, cast
from jose import JWTError, jwt
from passlib.context import CryptContext
from ...models.auth.user import User, UserInDB, TokenData, UserRole
from ...DB.database import get_database
from ..base import BaseService

# JWT settings
SECRET_KEY = "your-secret-key"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService(BaseService):
    def __init__(self):
        super().__init__("users")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash."""
        return pwd_context.hash(password)
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get a user by email."""
        collection = await self.get_collection()
        user_dict = await collection.find_one({"email": email})
        return UserInDB.model_validate(user_dict) if user_dict else None
    
    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
            
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Optional[User]:
        """Authenticate a user and return user object if successful."""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    async def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from JWT token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            email = payload.get("email")
            role = payload.get("role")
            
            if user_id is None or email is None or role is None:
                return None
                
            token_data = TokenData(
                user_id=cast(str, user_id),
                email=cast(str, email),
                role=UserRole(role)
            )
        except (JWTError, ValueError):
            return None
            
        user = await self.get_by_id(token_data.user_id)
        if user is None:
            return None
            
        return User.model_validate(user)
    
    async def create_user_token(self, user: User) -> str:
        """Create an access token for a user."""
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role
            },
            expires_delta=access_token_expires
        )
        return access_token 