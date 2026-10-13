import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(password : str): #Using BCrypt to hash the password, One way hashing
    #A Salt is a random data fed into a one way hashing function to ensure that the output (the hash) is unique even for identical inputs (passwords).
    #Cost is the number of rounds of hashing to apply, higher cost means more security but more time to compute the hash.
    cost = 12 #Cost factor, higher means more secure but slower
    salt = bcrypt.gensalt(rounds=cost)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) #Hashing algorithm requires bytes, encode the password to bytes using utf-8 encoding
    return hashed_password.decode('utf-8') #return the hashed password as a string, decode the bytes back to string using utf-8 encoding


def verify_password(password : str, hashed_password : str):
    #No salt is needed for bcrypt because the salt is automatically generated and stored as part
    #of the hashed password. When you verify a password, bcrypt extracts the salt from the stored hash and uses it to hash the provided password for comparison.
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(user_id : int):
    #The JWT Token consists of HEADER.PAYLOAD.SIGNATURE
    expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES) #Creates the DateTime Variable 30 Minutes from the Current Time

    jwt_payload = {
        "sub": str(user_id),
        "exp": expire
        }

    return jwt.encode(payload=jwt_payload,
                      key=SECRET_KEY,
                      algorithm=ALGORITHM)
