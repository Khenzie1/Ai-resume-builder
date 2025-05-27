from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.password_reset import PasswordResetRequest, PasswordResetConfirm
from app.api.deps import get_db
from app.crud import user as crud_user
# Removed: from app.core.security import create_access_token, verify_token - no longer needed for code-based reset
from app.services.email import send_reset_email
import random # Added for generating the 6-digit code

router = APIRouter()

@router.post("/forgot")
def forgot_password(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a 6-digit code
    reset_code = str(random.randint(100000, 999999))
    # Store the code and its expiry in the database
    crud_user.set_password_reset_code(db, user, reset_code)
    
    # Send the 6-digit code to the user's email
    send_reset_email(to_email=payload.email, code=reset_code)
    
    return {"message": "Password reset code has been sent to your email."}

@router.post("/reset")
def reset_password(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    # Verify the provided code against the stored one
    # This line now correctly accesses 'payload.email' because the schema will define it.
    if not crud_user.verify_reset_code(db, payload.email, payload.code):
        raise HTTPException(status_code=400, detail="Invalid or expired reset code.")

    success = crud_user.update_user_password(db, payload.email, payload.new_password)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or password update failed.")
    
    # Clear the reset code and expiry after successful password reset
    user = crud_user.get_user_by_email(db, payload.email) # Re-fetch user to ensure latest state
    if user:
        crud_user.clear_reset_code(db, user)
        
    return {"message": "Password has been reset successfully."}




# from fastapi import APIRouter, HTTPException, status, Depends
# from pydantic import BaseModel, EmailStr
# from sqlalchemy.orm import Session

# from app.api.deps import get_db
# from app.db.models.user import User
# from app.services import password_reset
# from app.core import email_utils

# router = APIRouter(prefix="/password-reset", tags=["Password Reset"])


# class PasswordResetRequest(BaseModel):
#     email: EmailStr


# class PasswordResetConfirm(BaseModel):
#     token: str
#     new_password: str


# @router.post("/request", status_code=200)
# def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == data.email).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User with this email does not exist."
#         )

#     token = password_reset.create_password_reset_token(user.email)
#     reset_link = f"http://localhost:8000/password-reset/confirm?token={token}"
#     try:
#         email_utils.send_reset_email(user.email, reset_link)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     return {"message": "Password reset link sent to your email."}


# @router.post("/confirm", status_code=200)
# def confirm_password_reset(data: PasswordResetConfirm, db: Session = Depends(get_db)):
#     user_email = password_reset.verify_reset_token(data.token)
#     if not user_email:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid or expired token."
#         )

#     user = db.query(User).filter(User.email == user_email).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found."
#         )

#     user.hashed_password = password_reset.hash_password(data.new_password)
#     db.commit()
#     return {"message": "Password has been reset successfully."}



