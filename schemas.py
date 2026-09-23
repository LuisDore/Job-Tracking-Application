from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date
from enums import StatusEnum

#USER SCHEMAS

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    email : EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str


#APPLICATION SCHEMAS

class ApplicationCreate(BaseModel):
    company_name : str
    job_title : str
    location : str | None = None
    salary : str | None = None
    status : StatusEnum
    date_applied : date | None = None
    notes : str | None = None
    job_url : str | None = None

class ApplicationUpdate(BaseModel):
    company_name: str | None = None
    job_title: str | None = None
    location: str | None = None
    salary: str | None = None
    status: StatusEnum | None = None
    date_applied: date | None = None
    notes: str | None = None
    job_url: str | None = None

class ApplicationResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True)

    application_id: int
    company_name: str 
    job_title: str 
    location: str | None
    salary: str | None
    status: StatusEnum
    date_applied: date | None
    notes: str | None
    job_url: str | None