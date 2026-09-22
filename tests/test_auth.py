from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
#TODO Set up Testing Database so the Main one isnt affected when running Tests
#TODO Write Tests for test_auth, test_applications, and conftest.py
#conftest.py is for test Fixtures such as a test database, a test Client, a test user, an auth jwt,  an auth client, You can define the setup once in conftest.py

def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Root endpoint"
    }

def test_registration():
    response = client.get("")

def test_duplicate_email():
    pass

def test_duplicate_username():
    pass

def test_login():
    pass

def test_wrong_password():
    pass

def test_invalid_jwt():
    pass

def test_expired_jwt():
    pass