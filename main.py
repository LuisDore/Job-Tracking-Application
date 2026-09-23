import fastapi as FastAPI
from DataBase import SessionLocal, engine
import models
import bcrypt
import jwt
from datetime import datetime, timedelta, date, timezone
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
import schemas

#Application :
#Application ID (Integer)
#Company Name (String)
#Job Title (String)
#Location (String)
#Salary (String)
#Status (String) - (Applied, Online Assessment, Interviewing, Offer, Rejected) Enum?
#Date Applied (Date)
#Notes (String)
#Job URL (String)


#200 OK
#201 Created
#400 Bad Request
#401 Unauthorized
#403 Forbidden
#404 Not Found
#409 Conflict
#422 Unprocessable Entity
#500 Internal Server Error

#To run the server do the following in the terminal:
#uvicorn FastAPI:app --reload

#TODO Database setup handled seperatly when i move to postGre

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-development-secret")
ALGORITHM = "HS256" #Symmetric Algorithm, uses the secret
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#bearer_scheme = HTTPBearer()


models.Base.metadata.create_all(bind=engine) #Creates the database tables based on the models defined in models.py

app = FastAPI.FastAPI() #Creates the FastAPI application instance

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme),
                    db = Depends(get_db)): # JWT -> Verify JWT -> Extract User ID -> Find User in DB -> Return User 

    #Function Flow:
    #JWT -> Verify JWT -> Extract User_ID -> Find User in DB with ID -> Return User if possible

    try:
        jwt_dict = jwt.decode(
            token,  #jwt.decode checks the validty of the token and returns differnt errors depening on the outcome
            key=SECRET_KEY, 
            algorithms=[ALGORITHM]
        ) #Decond the Toekn using the stated Algorithm
    except jwt.ExpiredSignatureError: #If the Token has expired 
        raise HTTPException(
            status_code=401,
            detail="JWT Expired"
        )  #When the HTTPException is raised it terminates any current functions running and wont run the rest of the code           
    except jwt.InvalidTokenError: #Token is otherwise Invalid, bad signature, malformed jwt, invalid claims.
        raise HTTPException(
            status_code=401,
            detail="Invalid Authentication Credentials"
        )

    user_id = jwt_dict.get("sub")

    try: 
        user_id = int(user_id)
    except(ValueError,TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authentication Credentials"
        )
        
    user = db.query(models.User).filter(models.User.user_id == int(user_id)).first() #Find user with the ID within the JWT from the db     

    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="User Not Found In Data Base"
        )

    return user



#User Authentication Endpoints
@app.post("/auth/register", response_model= schemas.UserResponse) #Register endpoint
def register_user(user_data : schemas.UserCreate, db = Depends(get_db)):
    #Check If the Username / Email is already in use
    
    check1 = (
        db.query(models.User)
        .filter(models.User.email == user_data.email)
        .first()
        )
    
    check2 = (
        db.query(models.User)
        .filter(models.User.username == user_data.username)
        .first()
        )
    
    if check1 is not None or check2 is not None:
        
        raise HTTPException(
            status_code=409,
            detail="Email or Username is already in use"
            )



    new_user = models.User(        
        username = user_data.username,
        email = user_data.email,
        hashed_password = hash_password(user_data.password), 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    

    return new_user

@app.post("/auth/login", response_model= schemas.Token) #Login endpoint
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):

    email = form_data.username #OAuth2 calls the credential username.
    password = form_data.password


    
    user = db.query(models.User).filter(models.User.email == email).first()
    

    #No salt is needed for bcrypt because the salt is automatically generated and stored as part 
    #of the hashed password. When you verify a password, bcrypt extracts the salt from the stored hash and uses it to hash the provided password for comparison.
    
    if user is None or not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')): #If the user doesnt exist or the passwords dont match 
       raise HTTPException(
           status_code=401,
           detail="Invalid Email or Password"
       )
       
    
    #The JWT Token consists of HEADER.PAYLOAD.SIGNATURE
    expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES) #Creates the DateTime Variable 30 Minutes from the Current Time (BST/GMT)

    jwt_payload = {
        "sub": str(user.user_id),
        "exp": expire            
        }
        
    encoded_jwt = jwt.encode(payload=jwt_payload, 
                                key=SECRET_KEY, 
                                algorithm=ALGORITHM) 
    
       
    return  {
            "access_token": encoded_jwt,
            "token_type": "bearer"}


#CRUD Endpoints for Applications
@app.get("/") #Root endpoint
def read_root():
    return {"message": "Root endpoint"}

@app.get("/applications",
        response_model=list[schemas.ApplicationResponse]
        ) #Gets all applications
def read_applications(current_user = Depends(get_current_user), db = Depends(get_db)):     
    applications = db.query(models.Application).filter(models.Application.user_id == current_user.user_id).all()   
    return applications

@app.post("/applications",
        response_model= schemas.ApplicationResponse) #Creates a new application   
def create_application(application : schemas.ApplicationCreate,
                        current_user = Depends(get_current_user),
                        db = Depends(get_db)):

    
    new_application = models.Application(        
        job_title= application.job_title,
        company_name= application.company_name,
        location= application.location,
        salary= application.salary,
        status= application.status,
        date_applied= application.date_applied,
        notes= application.notes,
        job_url= application.job_url,
        user_id= current_user.user_id  # Use the logged-in user's ID

    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    

    return new_application
    

@app.get("/applications/{application_id}",
        response_model=schemas.ApplicationResponse) #Gets a specific application by ID
def read_application(application_id: int, 
                    current_user = Depends(get_current_user),
                    db = Depends(get_db)):

    
    application = db.query(models.Application).filter(models.Application.application_id == application_id, 
                                                      models.Application.user_id == current_user.user_id).first()
    

    if application is None:
        raise HTTPException(status_code=404, 
                            detail="Application not found")

    return application

@app.put("/applications/{application_id}",
        response_model=schemas.ApplicationResponse) #Updates a specific application by ID
def update_application(application_id: int,
                       update_data : schemas.ApplicationUpdate,
                       current_user = Depends(get_current_user),
                       db = Depends(get_db)):    

   
    db_application = db.query(models.Application).filter(models.Application.application_id == application_id, 
                                                      models.Application.user_id == current_user.user_id).first()
    
    if db_application is None:
        raise HTTPException(status_code=404,
                            detail="Application not found")      

    to_update = {
        "job_title": update_data.job_title,
        "company_name": update_data.company_name,
        "location": update_data.location,
        "salary": update_data.salary,
        "status": update_data.status,
        "date_applied": update_data.date_applied,
        "notes": update_data.notes,
        "job_url": update_data.job_url
    }

    for key, value in to_update.items():
        if value is not None:
            setattr(db_application, key, value)

    db.commit()
    db.refresh(db_application)
    
    return db_application
    

@app.delete("/applications/{application_id}") #Deletes a specific application by ID
def delete_application(application_id: int, 
                       current_user = Depends(get_current_user),
                       db = Depends(get_db)):

    
    application = db.query(models.Application).filter(models.Application.application_id == application_id, 
                                                      models.Application.user_id == current_user.user_id).first()
    
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(application)
    db.commit()   
    return {"message": f"Application with ID {application_id} deleted successfully."}
    


#Buiseness Logic

def hash_password(password : str): #Using BCrypt to hash the password, One way hashing 
    #A Salt is a random data fed into a one way hashing function to ensure that the output (the hash) is unique even for identical inputs (passwords).
    #Cost is the number of rounds of hashing to apply, higher cost means more security but also more time to compute the hash.
    cost = 12 #Cost factor, higher means more secure but slower    
    salt = bcrypt.gensalt(rounds=cost)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) #Hashing algorithm requires bytes, encode the password to bytes using utf-8 encoding
    return hashed_password.decode('utf-8') #return the hashed password as a string, decode the bytes back to string using utf-8 encoding


