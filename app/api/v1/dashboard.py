from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.user import get_user_by_email
from app.crud.resume import get_user_resumes
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

@router.get("/")
def user_dashboard(db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    resumes = get_user_resumes(db, user.id)
    total_versions = len(resumes)
    versions_info = [{"id": r.id, "version": r.version, "created_at": r.created_at} for r in resumes]

    return {
        "user": {"id": user.id, "email": user.email, "created_at": user.created_at},
        "resume_count": total_versions,
        "resume_versions": versions_info
    }
