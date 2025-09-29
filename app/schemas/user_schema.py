from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterSchema(BaseModel):
    full_name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Full name must be between 3 and 50 characters",
    )
    email: EmailStr = Field(
        ...,
        description="Email must be a valid email address",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        description="Password must be between 8 and 50 characters",
    )

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    role: str
    access_token: Optional[str] = None

    class Config:
        from_attributes = True  # allows conversion from ORM models


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str
