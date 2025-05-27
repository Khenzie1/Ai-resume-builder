import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.api.deps import get_db

# Use SQLite for isolated test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./GIDE.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override for database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the tables before tests start
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# Provide a reusable test client
@pytest.fixture(scope="function")
def client():
    return TestClient(app)

# Helper to register and log in a user, returns access token
@pytest.fixture
def get_auth_token(client):
    def _get_token(email="test@example.com", password="secret123"):
        client.post("/api/v1/auth/register", json={"email": email, "password": password})
        res = client.post("/api/v1/auth/login", data={"username": email, "password": password})
        return res.json()["access_token"]
    return _get_token
