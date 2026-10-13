import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY, ALGORITHM
from app.database import get_db
import app.models as models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme),
                    db = Depends(get_db)): # JWT -> Verify JWT -> Extract User ID -> Find User in DB -> Return User

    #Function Flow:
    #JWT -> Verify JWT -> Extract User_ID -> Find User in DB with ID -> Return User if possible

    try:
        jwt_dict = jwt.decode(
            token,  #jwt.decode checks the validty of the token and returns differnt errors depening on the outcome
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        ) #Decode the Token using the stated Algorithm
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

    user = db.query(models.User).filter(models.User.user_id == user_id).first() #Find user with the ID within the JWT from the db

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User Not Found In Data Base"
        )

    return user
