from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import app.models as models
import app.schemas as schemas
from app.database import get_db
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model= schemas.UserResponse, status_code=201) #Register endpoint
def register_user(user_data : schemas.UserCreate, db = Depends(get_db)):
    #Check If the Username / Email is already in use

    check1 = (
        db.query(models.User)
        .filter(models.User.email == user_data.email)
        .first()
        )

    check2 = (
        db.query(models.User)
        .filter(models.User.username == user_data.username)
        .first()
        )

    if check1 is not None or check2 is not None:

        raise HTTPException(
            status_code=409,
            detail="Email or Username is already in use"
            )

    new_user = models.User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model= schemas.Token) #Login endpoint
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):

    email = form_data.username #OAuth2 calls the credential username.
    password = form_data.password

    user = db.query(models.User).filter(models.User.email == email).first()

    if user is None or not verify_password(password, user.hashed_password): #If the user doesnt exist or the passwords dont match
       raise HTTPException(
           status_code=401,
           detail="Invalid Email or Password"
       )

    return {
            "access_token": create_access_token(user.user_id),
            "token_type": "bearer"}
