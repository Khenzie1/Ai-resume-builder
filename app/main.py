from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, resume, dashboard
from app.api.v1.password_reset.routes import router as password_reset_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

app = FastAPI(
    title="GIDE",
    description="Generate ATS-ready, globally optimized resumes with AI",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(password_reset_router, prefix="/api/v1/password-reset", tags=["Password Reset"])
app.include_router(resume.router, prefix="/api/v1/resume", tags=["Resume"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {"message": "Welcome to GIDE"}
