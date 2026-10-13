from fastapi import FastAPI
from app.database import engine
import app.models as models
from app.routers import auth, applications

#To run the server do the following in the terminal:
#uvicorn app.main:app --reload

models.Base.metadata.create_all(bind=engine) #Creates the database tables based on the models defined in models.py

app = FastAPI() #Creates the FastAPI application instance

app.include_router(auth.router)
app.include_router(applications.router)


@app.get("/") #Root endpoint
def read_root():
    return {"message": "Root endpoint"}
