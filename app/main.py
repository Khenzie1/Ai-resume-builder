from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, resume, dashboard
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

app = FastAPI(
    title="AI Resume Generator",
    description="Generate ATS-ready, globally optimized resumes with AI",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(resume.router, prefix="/api/v1/resume", tags=["Resume"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {"message": "Welcome to the AI Resume Generator API"}
