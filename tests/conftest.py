import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from database import Base, engine, SessionLocal
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from users.models import User
from auth import get_password_hash

# ...

@pytest.fixture(scope="session")
def db_engine():
    return engine

@pytest.fixture(scope="session")
def db_session(db_engine):
    session = SessionLocal()
    yield session
    session.close()

@pytest_asyncio.fixture(scope="module")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def auth_headers(db_session):
    # Get or create a user for testing
    user = db_session.query(User).filter(User.username == "testuser").first()
    if not user:
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=get_password_hash("12345"), # Consistent with requirement
            bio="Test User",
            avatar_url="http://example.com/avatar.jpg"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}
