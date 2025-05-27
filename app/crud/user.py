from sqlalchemy.orm import Session
from app.db.models import user as models
from app.schemas import user as schemas
from app.core.security import hash_password
from datetime import datetime, timedelta

def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_pw = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, email: str, new_password: str) -> bool:
    user = get_user_by_email(db, email)
    if user:
        user.hashed_password = hash_password(new_password)
        db.commit()
        return True
    return False

def set_password_reset_code(db: Session, user: models.User, code: str):
    user.reset_code = code
    # Set code expiry to 20 minutes from now
    user.reset_code_expiry = datetime.utcnow() + timedelta(minutes=20)
    db.commit()
    db.refresh(user)

def verify_reset_code(db: Session, email: str, code: str) -> bool:
    user = get_user_by_email(db, email)
    # Check if user exists, code matches, and code has not expired
    if not user or user.reset_code != code:
        return False
    if not user.reset_code_expiry or user.reset_code_expiry < datetime.utcnow():
        return False
    return True

def clear_reset_code(db: Session, user: models.User):
    user.reset_code = None
    user.reset_code_expiry = None
    db.commit()
    db.refresh(user)