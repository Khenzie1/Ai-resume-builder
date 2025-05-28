# app/services/auth.py
import firebase_admin.auth
from datetime import datetime
import uuid # For generating placeholder password for new users

from sqlalchemy.orm import Session # Added for database session dependency

from app.db.models.user import User # User model for type hinting
from app.crud.user import get_user_by_email, create_user
from app.core.security import create_access_token
from app.schemas.user import UserCreate # Assuming this schema exists for create_user

# It's assumed that firebase_admin.initialize_app() has been called elsewhere in your application startup.

async def handle_google_signin(db: Session, firebase_id_token: str):
    """
    Verifies the Firebase ID token, and either logs in an existing user
    or creates a new user in your database.
    Returns user data and an application-specific access token.
    """
    try:
        decoded_token = firebase_admin.auth.verify_id_token(firebase_id_token)

        firebase_email = decoded_token.get("email")
        firebase_name = decoded_token.get("name") # Fetched from Firebase
        firebase_picture = decoded_token.get("picture") # Fetched from Firebase

        if not firebase_email:
            # Consider using HTTPException for API responses in a framework like FastAPI
            raise ValueError("Firebase token does not contain an email.")

        # Call synchronous CRUD function without await
        existing_user = get_user_by_email(db=db, email=firebase_email)
        
        user_for_token_and_response: User # To hold either existing_user or new_user

        if existing_user:
            # User exists in your database
            # You might want to update their details (e.g., name/picture from Firebase)
            # if your User model has corresponding fields and you wish to keep them synced.
            # For example, if User model had 'profile_picture_url' and 'display_name':
            # if firebase_name and existing_user.display_name != firebase_name:
            #     existing_user.display_name = firebase_name
            # if firebase_picture and existing_user.profile_picture_url != firebase_picture:
            #     existing_user.profile_picture_url = firebase_picture
            # await db.commit() # If using SQLAlchemy async session
            # db.commit() # For synchronous SQLAlchemy session, after potential updates

            user_for_token_and_response = existing_user
            
            # The User model provided does not have a 'role' field.
            # Role-based access control logic has been removed.
            # If roles were present:
            # if existing_user.role == AccountType.user or existing_user.role == AccountType.case_officer:
            #    pass # Proceed
            # else:
            #    raise ValueError("Unauthorized role for this sign-in method.")

        else:
            # New user signing up
            # The User model requires a non-null hashed_password.
            # For social logins, a password isn't typically set by the user in our system.
            # This is a workaround: generate a random, unusable password.
            # Ideally, User.hashed_password should be nullable or a separate creation
            # path for social users should exist that doesn't require a password.
            
            # Assuming app.schemas.user.UserCreate looks like:
            # class UserCreate(BaseModel):
            #     email: EmailStr
            #     password: str
            #     # full_name: Optional[str] = None # If User model/create_user supports it
            
            # Note: The provided User model does not have a 'full_name' field.
            # If it did, and UserCreate schema supported it, you could pass firebase_name:
            # user_create_payload = UserCreate(email=firebase_email, password=str(uuid.uuid4()), full_name=firebase_name)
            user_create_payload = UserCreate(email=firebase_email, password=str(uuid.uuid4()))

            # Call synchronous CRUD function without await
            new_user = create_user(db=db, user=user_create_payload)
            user_for_token_and_response = new_user

        # Prepare data for the access token
        # The User model does not have 'role', so it's omitted from the token.
        access_token_data = {
            "sub": str(user_for_token_and_response.id),
            "email": user_for_token_and_response.email
        }
        access_token = create_access_token(data=access_token_data)

        # Prepare user data for the response
        # Includes fields directly from the User model and supplements with Firebase data
        # The User model does not have 'full_name', 'updated_at', or 'role'.
        user_response_data = {
            "user_id": str(user_for_token_and_response.id),
            "email": user_for_token_and_response.email,
            "full_name": firebase_name,  # Name from Firebase token
            "picture": firebase_picture, # Picture from Firebase token
            "created_at": user_for_token_and_response.created_at.isoformat(),
            # "updated_at" is not in the User model
            # "role" is not in the User model
        }
            
        return {"user": user_response_data, "access_token": access_token}

    except firebase_admin.auth.InvalidIdTokenError as e:
        # Log the error for debugging
        print(f"Invalid Firebase ID token: {e}")
        # In a web framework, you'd typically raise an HTTPException here
        raise ValueError("Invalid or expired Firebase ID token.")
    except ValueError as e: # Catching specific ValueErrors raised above
        print(f"Authentication business logic error: {e}")
        raise # Re-raise to be handled by the caller (e.g., API route)
    except Exception as e:
        # Log the error for debugging
        print(f"An unexpected error occurred during Google Sign-In: {e}")
        # In a web framework, you'd typically raise an HTTPException here
        raise ValueError(f"Authentication failed due to an unexpected error.")

