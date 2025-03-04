from passlib.context import CryptContext
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Security
from backend.database import users_collection

load_dotenv() # Load environment variables from .env file

# Environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    """ Hashes the password """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verifies the password """
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt(user_id: str, role: str) -> str:
    """ Creates a JWT token """
    return jwt.encode({"sub": user_id, "role": role}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Security(oauth2_scheme)):
    """ Gets the current user """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # Decode the token
        user_id: str = payload.get("sub") # Get the user_id
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token not valid")
        user = users_collection.find_one({"user_id": user_id}) # Find the user
        if not user: # If the user is not found
            raise HTTPException(status_code=401, detail="User not found")
        return user # If the user is found, return the user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token not valid")
