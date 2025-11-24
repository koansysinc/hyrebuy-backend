"""
Pydantic schemas for User API requests and responses
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    company_id: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user data in responses"""
    id: str
    phone: Optional[str]
    company_id: Optional[str]
    is_group_admin: str  # String for Phase 1 MVP ("true" or "false")
    total_rewards_earned: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token payload"""
    email: Optional[str] = None


class AuthResponse(BaseModel):
    """Schema for authentication response (login/register)"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
