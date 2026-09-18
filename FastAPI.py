import fastapi as FastAPI
from DataBase import SessionLocal, engine
import models


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

app = FastAPI.FastAPI()

Base = models.Base
Base.metadata.create_all(bind=engine)

#User Authentication Endpoints
@app.post("/auth/Register") #Register endpoint
def register_user():
    pass

@app.post("/auth/Login") #Login endpoint
def login_user():
    pass




#CRUD Endpoints for Applications
@app.get("/") #Root endpoint
def read_root():
    return {"message": "Root endpoint"}

@app.get("/applications") #Gets all applications
def read_applications():
    db = SessionLocal()
    applications = db.query(models.Application).all()
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
                        job_url: str,
                        user_id: int):
    
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
        user_id= user_id

    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    db.close()

    return new_application

@app.get("/applications/{application_id}") #Gets a specific application by ID
def read_application(application_id: int):

    db = SessionLocal()
    application = db.query(models.Application).filter(models.Application.application_id == application_id).first()
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
    
    db = SessionLocal()
    application = db.query(models.Application).filter(models.Application.application_id == application_id).first()
    
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

    db = SessionLocal()
    application = db.query(models.Application).filter(models.Application.application_id == application_id).first()
    
    if application:
        db.delete(application)
        db.commit()
        db.close()
        return {"message": f"Application with ID {application_id} deleted successfully."}
    else:
        db.close()
        return {"message": f"Application with ID {application_id} not found."}


#Buiseness Logic
