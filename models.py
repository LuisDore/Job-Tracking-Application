from sqlalchemy import Boolean, Column, Integer, String
from DataBase import Base

class Task(Base):
    __tablename__ = "tasks"

    application_id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)