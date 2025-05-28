from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.crud import user as crud_user
from app.core.security import verify_password, create_access_token
from app.api.deps import get_db
from app.services.auth import handle_google_signin # Import the service function
from app.schemas.firebase_schemas import FirebaseTokenRequest, AuthSuccessResponse

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Corrected call: Pass user_data.email as a positional argument
    db_user = crud_user.get_user_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user=user_data)

@router.post("/login")  
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Corrected call: Pass user_data.email as a positional argument
    user = crud_user.get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/google-signin", response_model=AuthSuccessResponse)
async def google_signin(request: FirebaseTokenRequest):
    """
    Handles Google Sign-In/Sign-Up by verifying the Firebase ID token.
    """
    try:
        result = await handle_google_signin(request.id_token)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )