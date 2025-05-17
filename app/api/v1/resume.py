from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.resume import ResumeCreate, ResumeOut
from app.crud import resume as crud_resume
from app.api.deps import get_db
from app.services.ai_resume import generate_resume_suggestions
from jose import JWTError
import jwt
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

@router.post("/", response_model=ResumeOut)
def create_resume(resume_data: ResumeCreate, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    from app.crud.user import get_user_by_email
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_resume.create_resume(db, user.id, resume_data)

@router.get("/", response_model=list[ResumeOut])
def list_resumes(db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    from app.crud.user import get_user_by_email
    user = get_user_by_email(db, user_email)
    return crud_resume.get_user_resumes(db, user.id)

@router.post("/ai-suggest")
def get_ai_suggestions(name: str, education: str, experience: str, skills: str, location: str):
    return generate_resume_suggestions(name, education, experience, skills, location)
