# from passlib.context import CryptContext
# from jose import JWTError, jwt

# from datetime import datetime, timedelta
# from app.core.config import settings

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt


#To achieve the secret key, 
# python -c "import secrets; print(secrets.token_urlsafe(32))"
#on your terminal



# from datetime import datetime, timedelta
# from jose import jwt, JWTError
# from passlib.context import CryptContext
# from typing import Optional
# from app.core.config import settings

# # Password hashing setup
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# # Access token generation
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt

# def decode_access_token(token: str) -> Optional[dict]:
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         return payload
#     except JWTError:
#         return None

# # Password reset token generation
# def create_password_reset_token(email: str) -> str:
#     delta = timedelta(hours=1)
#     expire = datetime.utcnow() + delta
#     to_encode = {"sub": email, "exp": expire}
#     return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# # Password reset token verification
# def verify_password_reset_token(token: str) -> Optional[str]:
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         return payload.get("sub")
#     except JWTError:
#         return None





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
    # It remains unchanged as per your request to keep initial task functionality.
    from jose import jwt # Imported locally to avoid global unused import if not needed elsewhere
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# General token verification (remains as is for general auth)
def verify_token(token: str) -> Optional[dict]:
    # This function is for general token verification, not password reset codes.
    # It remains unchanged as per your request to keep initial task functionality.
    from jose import jwt, JWTError # Imported locally
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

# Removed: create_password_reset_token and verify_password_reset_token as they are replaced by 6-digit code mechanism.