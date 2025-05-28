from datetime import datetime, timedelta
from typing import Optional

# Removed: from jose import jwt, JWTError - no longer needed for code-based reset
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Access token generation (remains as is for general auth)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # This function is for general access tokens, not password reset codes.
    from jose import jwt # Imported locally to avoid global unused import if not needed elsewhere
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# General token verification (remains as is for general auth)
def verify_token(token: str) -> Optional[dict]:
    from jose import jwt, JWTError # Imported locally
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
