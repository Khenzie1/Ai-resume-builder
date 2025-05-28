from sqlalchemy.orm import Session
from app.db.models import user as models
from app.db.models.user import User
from app.schemas import user as schemas
from app.core.security import hash_password
from datetime import datetime, timedelta

# This is the correct synchronous version you should be using
def get_user_by_email(db: Session, email: str) -> models.User | None: # Added | None for clarity on return type
    """
    Retrieves a user from the database by their email address.
    """
    return db.query(models.User).filter(models.User.email == email).first()

# This is the correct synchronous version you should be using
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Creates a new user in the database.
    """
    hashed_pw = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, email: str, new_password: str) -> bool:
    """
    Updates the password for a user.
    """
    user = get_user_by_email(db, email)
    if user:
        user.hashed_password = hash_password(new_password)
        db.commit()
        return True
    return False

def set_password_reset_code(db: Session, user: models.User, code: str):
    """
    Sets a password reset code for a user with an expiry time.
    """
    user.reset_code = code
    # Set code expiry to 20 minutes from now
    user.reset_code_expiry = datetime.utcnow() + timedelta(minutes=20)
    db.commit()
    db.refresh(user)

def verify_reset_code(db: Session, email: str, code: str) -> bool:
    """
    Verifies if a given reset code for an email is valid and not expired.
    """
    user = get_user_by_email(db, email)
    # Check if user exists, code matches, and code has not expired
    if not user or user.reset_code != code:
        return False
    if not user.reset_code_expiry or user.reset_code_expiry < datetime.utcnow():
        return False
    return True

def clear_reset_code(db: Session, user: models.User):
    """
    Clears the password reset code and its expiry for a user.
    """
    user.reset_code = None
    user.reset_code_expiry = None
    db.commit()
    db.refresh(user)