import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app, get_db
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)



#Used to override the normal get_db() so the tests know to use the testing database

client = TestClient(app)


@pytest.fixture(scope="function") #
def db():
    Base.metadata.create_all(bind = engine) #Creates the database tables based on Base

    db = TestingSessionLocal() #Creates the database session

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bine = engine)


@pytest.fixture(scope="function")
def client(db):

    def override_get_db():    
        try: 
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()