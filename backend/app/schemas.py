from pydantic import BaseModel, Field
from typing import Optional
from pydantic import field_validator

class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role_id: Optional[int] = 1

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("email")
    def email_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Email cannot be empty")
        return v.strip()

    @field_validator("password")
    def password_not_empty(cls, v):
        if not v:
            raise ValueError("Password cannot be empty")
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        if len(v.encode('utf-8')) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")
        return v

    @field_validator("role_id")
    def role_id_valid(cls, v):
        if v not in [1, 2]:
            raise ValueError("Role ID must be 1 (user) or 2 (admin)")
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None

    @field_validator("role_id")
    def role_id_valid(cls, v):
        if v is not None and v not in [1, 2]:
            raise ValueError("Role ID must be 1 (user) or 2 (admin)")
        return v


class UserResponse(BaseModel):
    id: int = Field(..., description="ID do usuário")
    name: str
    email: str
    role_id: int
    role: RoleResponse

    @field_validator("id")
    def id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("ID must be a positive integer")
        return v

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    def email_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Email cannot be empty")
        return v.strip()

    @field_validator("password")
    def password_not_empty(cls, v):
        if not v:
            raise ValueError("Password cannot be empty")
        return v

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = "bearer"
    user: UserResponse = Field(..., description="User information")
