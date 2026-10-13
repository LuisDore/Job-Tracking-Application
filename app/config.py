import os
from dotenv import load_dotenv

load_dotenv() #Loads variables from the .env file (git ignored) into the environment

SECRET_KEY = os.environ["JWT_SECRET_KEY"] #No fallback, the app refuses to start without a real key
ALGORITHM = "HS256" #Symmetric Algorithm, uses the secret
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#TODO Database setup handled seperatly when i move to postGre
DATABASE_URL = "sqlite:///./Applications.db"
