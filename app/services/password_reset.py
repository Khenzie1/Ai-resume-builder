from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.password_reset import PasswordResetRequest, PasswordResetConfirm
from app.api.deps import get_db
from app.crud import user as crud_user
from app.services.email import send_reset_email
import random # Added for generating the 6-digit code

router = APIRouter()

@router.post("/forgot")
def forgot_password(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_code = str(random.randint(100000, 999999))  # 6-digit code
    crud_user.set_password_reset_code(db, user, reset_code)
    # Pass the code to the email service
    send_reset_email(to_email=payload.email, code=reset_code)

    return {"message": "Reset code sent to your email."}

@router.post("/reset")
def reset_password(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    # Verify the provided code against the stored one
    if not crud_user.verify_reset_code(db, payload.email, payload.code): # Changed payload.token to payload.code
        raise HTTPException(status_code=400, detail="Invalid or expired reset code.")

    success = crud_user.update_user_password(db, payload.email, payload.new_password)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    # Clear the code after use
    user = crud_user.get_user_by_email(db, payload.email) # Re-fetch user to ensure latest state
    if user:
        crud_user.clear_reset_code(db, user)

    return {"message": "Password has been reset successfully."}