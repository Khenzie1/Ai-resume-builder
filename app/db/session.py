from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

#for sqlite
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
# New (for PostgreSQL)
# engine = create_engine(
#     settings.DATABASE_URL#, pool_pre_ping=True # Removed connect_args={"check_same_thread": False}
# )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
