import fastapi as FastAPI
from DataBase import SessionLocal, engine
import models
import bcrypt

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

#To run the server do the following in the terminal:
#uvicorn FastAPI:app --reload


logged_in_user = None #Global variable to store the logged in user's username


app = FastAPI.FastAPI() #Creates the FastAPI application instance

Base = models.Base #Creates the Base class for the SQLAlchemy models
Base.metadata.create_all(bind=engine) #Creates the database tables based on the models defined in models.py

#User Authentication Endpoints
@app.post("/auth/Register") #Register endpoint
def register_user(new_username: str, new_email: str, password: str):
    db = SessionLocal()

    new_user = models.User(
        user_id = db.query(models.User).count() + 1, #Auto Incrementing User ID 
        username = new_username,
        email = new_email,
        hashed_password = Hash(password), 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

@app.post("/auth/Login") #Login endpoint
def login_user(email: str, password: str):
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.email == email).first()
    db.close()
    #No salt is needed for bcrypt because the salt is automatically generated and stored as part 
    #of the hashed password. When you verify a password, bcrypt extracts the salt from the stored hash and uses it to hash the provided password for comparison.
    if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')): #If the user exists and the password matches the hashed password in the database
       
        global logged_in_user
        logged_in_user = user #Store the logged in user
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid email or password"}

#CRUD Endpoints for Applications
@app.get("/") #Root endpoint
def read_root():
    return {"message": "Root endpoint"}

@app.get("/applications") #Gets all applications
def read_applications():

    if logged_in_user is None: #If the user is not logged in, return an error message
        return {"message": "User not logged in. Please log in to view applications."}

    db = SessionLocal()
    applications = db.query(models.Application).filter(models.Application.user_id == logged_in_user.user_id).all()
    db.close()
    return applications

@app.post("/applications") #Creates a new application   
def create_application(title: str, 
                        company: str,
                        location: str,
                        salary: str,
                        status: models.StatusEnum,
                        date_applied: str, 
                        notes: str,
                        job_url: str):
    
    if logged_in_user is None: #If the user is not logged in, return an error message
        return {"message": "User not logged in. Please log in to create applications."}


    db = SessionLocal()
    new_application = models.Application(
        application_id= db.query(models.Application).count() + 1,  # Auto-incrementing application_id
        job_title= title,
        company_name= company,
        location= location,
        salary= salary,
        status= status,
        date_applied= date_applied,
        notes= notes,
        job_url= job_url,
        user_id= logged_in_user.user_id  # Use the logged-in user's ID

    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    db.close()

    return new_application

@app.get("/applications/{application_id}") #Gets a specific application by ID
def read_application(application_id: int):

    if logged_in_user is None: #If the user is not logged in, return an error message
        return {"message": "User not logged in. Please log in to view an application."}

    db = SessionLocal()
    application = db.query(models.Application).filter(models.Application.application_id == application_id, 
                                                      models.Application.user_id == logged_in_user.user_id).first()
    db.close()

    return application

@app.put("/applications/{application_id}") #Updates a specific application by ID
def update_application(application_id: int, 
                       title: str = None, 
                       company: str = None,
                       location: str = None,
                       salary: str = None,
                       status: models.StatusEnum = None,
                       date_applied: str = None, 
                       notes: str = None,
                       job_url: str = None):    
    
    if logged_in_user is None: #If the user is not logged in, return an error message
        return {"message": "User not logged in. Please log in to update an application."}

    db = SessionLocal()
    application = db.query(models.Application).filter(models.Application.application_id == application_id, 
                                                      models.Application.user_id == logged_in_user.user_id).first()
    
    if application:        

        to_update = {
            "job_title": title,
            "company_name": company,
            "location": location,
            "salary": salary,
            "status": status,
            "date_applied": date_applied,
            "notes": notes,
            "job_url": job_url
        }

        for key, value in to_update.items():
            if value is not None:
                setattr(application, key, value)

        db.commit()
        db.refresh(application)
        db.close()
        return application

    else:
        db.close()
        return {"message": f"Application with ID {application_id} not found."}

@app.delete("/applications/{application_id}") #Deletes a specific application by ID
def delete_application(application_id: int):

    if logged_in_user is None: #If the user is not logged in, return an error message
        return {"message": "User not logged in. Please log in to delete an application."}

    db = SessionLocal()
    application = db.query(models.Application).filter(models.Application.application_id == application_id, 
                                                      models.Application.user_id == logged_in_user.user_id).first()
    
    if application:
        db.delete(application)
        db.commit()
        db.close()
        return {"message": f"Application with ID {application_id} deleted successfully."}
    else:
        db.close()
        return {"message": f"Application with ID {application_id} not found."}


#Buiseness Logic

def Hash(password : str): #Using BCrypt to hash the password, One way hashing 
    #A Salt is a random data fed into a one way hashing function to ensure that the output (the hash) is unique even for identical inputs (passwords).
    #Cost is the number of rounds of hashing to apply, higher cost means more security but also more time to compute the hash.
    cost = 12 #Cost factor, higher means more secure but slower    
    salt = bcrypt.gensalt(rounds=cost)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) #Hashing algorithm requires bytes, encode the password to bytes using utf-8 encoding
    return hashed_password.decode('utf-8') #return the hashed password as a string, decode the bytes back to string using utf-8 encoding
