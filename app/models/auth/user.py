from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from ..base import BaseDBModel, StatusModel

class UserRole(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.STUDENT

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None

class User(BaseDBModel, StatusModel):
    email: EmailStr
    hashed_password: str
    full_name: str
    role: UserRole = UserRole.STUDENT
    status: UserStatus = UserStatus.ACTIVE
    enrolled_courses: List[str] = Field(default_factory=list)
    teaching_courses: List[str] = Field(default_factory=list)

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "role": "student",
                "status": "active",
                "enrolled_courses": [],
                "teaching_courses": []
            }
        }

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: str
    email: str
    role: UserRole 