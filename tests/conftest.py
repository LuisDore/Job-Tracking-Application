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
        yield db #returns the newly setup Database for the test client
    finally:
        db.close()
        Base.metadata.drop_all(bind = engine) #after the the other fixture and the test function has completed, the database is closed and deleted so the next test can have a fresh database.


@pytest.fixture(scope="function")
def client(db):

    def override_get_db():#the overidden get_db() function returns the new testing Database made above
        try: 
            yield db #returns the testing db for the API endpoints
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db #Changes which dependancy FastAPI uses to satify Depends(get_db)

    #"with" is used for resource management, it ensures the client doesnt stay open after each test in completed, it automatically handles the clean up process
    with TestClient(app) as client: #TestClient allows pytest to communicate with FastAPI and can simulate HTTP Requests
        yield client

    app.dependency_overrides.clear() #Removes all temporary dependancy overrides made so it doesnt interfere with the main application.


@pytest.fixture(scope="function")
def user_test():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Password123!"
    }


@pytest.fixture(scope="function")
def register_user(client, user_test):
    response = client.post("/auth/register", json=user_test)
    return response, user_test