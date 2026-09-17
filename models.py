
from enum import Enum
from sqlalchemy import Boolean, Column, Integer, String
from DataBase import Base

class StatusEnum(Enum):
    APPLIED = "Applied"
    ONLINE_ASSESSMENT = "Online Assessment"
    INTERVIEWING = "Interviewing"
    OFFER = "Offer"
    REJECTED = "Rejected"

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


class Application(Base):
    __tablename__ = "applications"

    application_id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    salary = Column(String, nullable=True)
    status = Column(StatusEnum, nullable=False) 
    date_applied = Column(String, nullable=True)  #TODO: Change to Date type if needed
    notes = Column(String, nullable=True)
    job_url = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False, foreign_key="users.user_id")  # Foreign key to the User table

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


