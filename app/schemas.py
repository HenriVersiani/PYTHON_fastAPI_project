from pydantic import BaseModel, Field
from typing import Optional
from pydantic import field_validator

class UserCreate(BaseModel):
    name: str
    email: str
    role: Optional[str] = "user"

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

    @field_validator("role")
    def role_valid(cls, v):
        valid_roles = ["user", "admin"]
        if v not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

    @field_validator("role")
    def role_valid(cls, v):
        if v is not None:
            valid_roles = ["user", "admin"]
            if v not in valid_roles:
                raise ValueError(f"Role must be one of {valid_roles}")
        return v


class UserResponse(BaseModel):
    id: int = Field(..., description="ID do usuário")
    name: str
    email: str
    role: str

    @field_validator("id")
    def id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("ID must be a positive integer")
        return v

    class Config:
        from_attributes = True
