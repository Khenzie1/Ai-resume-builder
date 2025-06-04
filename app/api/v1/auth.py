from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.crud import user as crud_user
from app.crud.user import get_user_by_email # Explicitly import get_user_by_email if used directly
from app.core.security import verify_password, create_access_token
from app.api.deps import get_db
from app.services.auth import handle_google_signin # Import the service function
from app.schemas.firebase_schemas import FirebaseTokenRequest, AuthSuccessResponse

router = APIRouter()

@router.get("/check-email")
def check_email_exists(email: str, db: Session = Depends(get_db)):
    """
    Checks if an email already exists in the database.
    Returns {"exists": True} if found, {"exists": False} otherwise.
    Always returns 200 OK.
    """
    user = crud_user.get_user_by_email(db, email)
    if user:
        return {"exists": True, "message": "Email found."}
    return {"exists": False, "message": "Email not found."}

@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user=user_data)

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/google-signin", response_model=AuthSuccessResponse)
async def google_signin(
    request: FirebaseTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Handles Google Sign-In by verifying the Firebase ID token.
    It relies on the 'handle_google_signin' service to enforce
    whether only registered users are allowed or if new users are auto-registered.
    """
    try:
        # Pass the injected 'db' session to the service function
        result = await handle_google_signin(db, request.id_token)
        return result
    except HTTPException as e:
        # Catch HTTPExceptions raised by handle_google_signin (e.g., 401 for unregistered users)
        raise e
    except ValueError as e:
        # Catch ValueErrors from the service layer (e.g., email missing from token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Catch any other unexpected errors from the service or during token verification
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during Google Sign-In: {e}",
        )
