
from sqlalchemy import Column, Enum as SQLAlchemyEnum, ForeignKey, Integer, String, Date
from DataBase import Base
from enums import StatusEnum


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
    location = Column(String, nullable= True)
    salary = Column(String, nullable=True)

    status = Column(
        SQLAlchemyEnum(StatusEnum),
        nullable=False
        )
    
    date_applied = Column(Date, nullable=True)  
    notes = Column(String, nullable=True)
    job_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


