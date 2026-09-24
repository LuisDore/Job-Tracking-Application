from .conftest import client
import jwt
from datetime import datetime, timedelta, timezone
from main import SECRET_KEY, ALGORITHM
#conftest.py is for test Fixtures such as a test database, a test Client, a test user, an auth jwt,  an auth client

###### Testing Regristration and Login Endpoints ######

def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Root endpoint"
    }

def test_registration(register_user):
    registration_response, user = register_user
    assert registration_response.status_code == 201

def test_duplicate_email(client, register_user): #Expecting 409 Conflict status code 
    registration_response, user = register_user
    assert registration_response.status_code == 201 #Successfull Creation of the first User

    response = client.post(   
         "/auth/register",
         json={
             "username": "testuser1", #Same Username
             "email": user["email"], #Different Email
             "password": user["password"]  #Password doesnt Matter as Two users can have the same password
         }
     )

    assert  response.status_code == 409
    assert response.json() == {"detail" : "Email or Username is already in use"}

def test_duplicate_username(client, register_user): #Expecting 409 Conflict status code 
    registration_response, user = register_user
    assert registration_response.status_code == 201 #Successfull Creation of the first User

    response = client.post(
        "/auth/register",
        json={
            "username": user["username"], #Same Username
            "email": "test1@example.com", #Different Email
            "password": user["password"]  #Password doesnt Matter as Two users can have the same password
        }
    )

    assert  response.status_code == 409
    assert response.json() == {"detail" : "Email or Username is already in use"}

def test_login(client, register_user):   
    registration_response, user = register_user
    assert registration_response.status_code == 201 #Successfull Creation of the first User

    response = client.post("/auth/login", #Oauth2 from calls the field "username" not "email"
                           data = {"username" : user["email"], #Called Data as OAuth2PasswordRequestFrom Expects form-encoded Data not JSON
                                   "password" : user["password"]})

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data #Checks the reponse JSON for an Access Token JWT
    assert data["token_type"] == "bearer" #Checks the reponse JSON for the Token Type Field

def test_wrong_password(client, register_user):
    registration_response, user = register_user
    assert registration_response.status_code == 201 #Successfull Creation of the first User
    
    response = client.post("/auth/login", #Oauth2 from calls the field "username" not "email"
                               data = {"username" : user["email"], #Called Data as OAuth2PasswordRequestFrom Expects form-encoded Data not JSON
                                       "password" : "Password"}) #Different Password to the Registered User

    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid Email or Password"}

def test_wrong_email(client, register_user):
    registration_response, user = register_user
    assert registration_response.status_code == 201 #Successfull Creation of the first User
        
    response = client.post("/auth/login", #Oauth2 from calls the field "username" not "email"
                                   data = {"username" : "test1@example.com", #Different username (Email) to the Registered User
                                           "password" : user["password"]}) 
    
    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid Email or Password"}

###### Testing of get_current_user() Dependency ######

def test_no_jwt(client):
    response = client.get("/applications")
    assert response.status_code == 401

def test_invalid_jwt(client):
    response = client.get("/applications",
                          headers={
                              "Authorization" : "Bearer Invalid Token"
                          })
    assert response.status_code == 401

def test_expired_jwt(client): #Need to create an expired JWT to pass

    expired_token = jwt.encode(
        {
            "sub": "1",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1) #Creates a token that Expired 1 minute ago
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response = client.get("/applications",
                          headers={
                              "Authorization": f"Bearer {expired_token}"
                          })

    assert response.status_code == 401
    assert response.json() == {"detail": "JWT Expired"}

