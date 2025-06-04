# app/services/auth.py
import firebase_admin.auth
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException, status # Required for raising HTTP errors

from app.db.models.user import User # User model for type hinting
from app.crud.user import get_user_by_email # Only need to get user, not create
# from app.crud.user import create_user # Not needed if you don't auto-register
# from app.schemas.user import UserCreate # Not needed if you don't auto-register

from app.core.security import create_access_token
from app.schemas.firebase_schemas import AuthSuccessResponse
from app.schemas.user import UserOut # Assuming your UserOut schema is defined

# It's assumed that firebase_admin.initialize_app() has been called elsewhere in your application startup.
# Example: In app/main.py or a dedicated app/core/firebase_config.py

async def handle_google_signin(db: Session, firebase_id_token: str) -> AuthSuccessResponse:
    """
    Verifies the Firebase ID token and logs in an existing user.
    
    IMPORTANT: This function DOES NOT automatically register new users.
    If the user's email from the Google token is not found in your database,
    an HTTPException (401 Unauthorized) is raised.
    
    Returns user data and an application-specific access token upon successful login.
    """
    try:
        # 1. Verify the Firebase ID token with Google's servers
        decoded_token = firebase_admin.auth.verify_id_token(firebase_id_token)

        firebase_email = decoded_token.get("email")
        # You can fetch other details if needed, but not used for login/registration check here
        # firebase_name = decoded_token.get("name")
        # firebase_picture = decoded_token.get("picture")

        if not firebase_email:
            # This should ideally not happen if Firebase token is valid for a Google account
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Firebase token does not contain a valid email."
            )

        # 2. Check if the user exists in your database by email
        existing_user = get_user_by_email(db=db, email=firebase_email)

        if not existing_user:
            # --- CRITICAL CHANGE FOR "REGISTERED USERS ONLY" POLICY ---
            # If the user's email from Google is NOT found in your database,
            # we raise an unauthorized error to prevent automatic registration.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not registered. Please register first or use standard login."
            )

        # If we reach here, the user *does* exist in your database
        user_for_token_and_response: User = existing_user

        # 3. Generate your application-specific access token
        # You might want to update the last_login timestamp here if you track it
        # user_for_token_and_response.last_login = datetime.utcnow()
        # db.add(user_for_token_and_response)
        # db.commit()
        # db.refresh(user_for_token_and_response)

        access_token_data = {
            "sub": str(user_for_token_and_response.id), # Use ID for robustness
            "email": user_for_token_and_response.email
        }
        access_token = create_access_token(data=access_token_data)

        # 4. Prepare user data for the response using UserOut schema
        # Ensure your UserOut schema has 'id', 'email', and 'username'
        # And that your User model also has a 'username' field.
        user_response_data = UserOut(
            id=user_for_token_and_response.id,
            email=user_for_token_and_response.email,
            username=user_for_token_and_response.username # Assuming User model has 'username'
            # Add other fields from your User model that are in UserOut
            # e.g., created_at=user_for_token_and_response.created_at
        )

        # 5. Return the AuthSuccessResponse object
        return AuthSuccessResponse(user=user_response_data, access_token=access_token)

    except firebase_admin.auth.InvalidIdTokenError as e:
        # Catch Firebase-specific token validation errors (e.g., token expired, malformed)
        print(f"DEBUG: Invalid Firebase ID token: {e}") # Log this for server-side debugging
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase ID token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException as e:
        # This catches HTTPExceptions explicitly raised within this function (like the 401 for unregistered users)
        raise e # Re-raise them to be handled by the FastAPI router
    except Exception as e:
        # Catch any other unexpected errors during the process
        print(f"ERROR: An unexpected error occurred during Google Sign-In: {e}") # Log for debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed due to an unexpected server error: {e}",
        )

