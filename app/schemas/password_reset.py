from pydantic import BaseModel, EmailStr, Field

class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")

class PasswordResetConfirm(BaseModel):
    # ADDED: The email field is now part of the confirmation payload
    email: EmailStr = Field(..., example="user@example.com", description="User's email for password reset confirmation")
    code: str = Field(..., min_length=6, max_length=6, example="123456", description="6-digit password reset code")
    new_password: str = Field(..., min_length=8, example="newStrongPassword123")
