from sqlalchemy.orm import Session
from app.db.models.resume import Resume
from app.schemas.resume import ResumeCreate

def create_resume(db: Session, user_id: int, resume_data: ResumeCreate):
    last_resume = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.version.desc()).first()
    new_version = (last_resume.version + 1) if last_resume else 1

    resume = Resume(user_id=user_id, content=resume_data.content, version=new_version)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume

def get_user_resumes(db: Session, user_id: int):
    return db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.version.desc()).all()
