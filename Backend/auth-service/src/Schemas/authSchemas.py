"""Pydantic schemas for Authentication."""

from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "alice@example.com",
                "password": "strong_password_123"
            }
        }
    }


class SignUpResponse(BaseModel):
    id: str
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "email": "alice@example.com"
            }
        }
    }


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    model_config = {
        "json_schema_extra": {
            "example": {"email": "alice@example.com", "password": "strong_password_123"}
        }
    }


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {
        "json_schema_extra": {
            "example": {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "token_type": "bearer"}
        }
    }


class LogoutResponse(BaseModel):
    message: str

    model_config = {
        "json_schema_extra": {
            "example": {"message": "Successfully logged out"}
        }
    }
