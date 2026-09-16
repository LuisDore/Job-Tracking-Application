import fastapi as FastAPI

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
    pass

@app.POST("/applications") #Creates a new application   
def create_application():
    pass

@app.get("/applications/{application_id}") #Gets a specific application by ID
def read_application(application_id: int):
    pass

@app.put("/applications/{application_id}") #Updates a specific application by ID
def update_application(application_id: int):    
    pass

@app.delete("/applications/{application_id}") #Deletes a specific application by ID
def delete_application(application_id: int):
    pass


#Buiseness Logic
