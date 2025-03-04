from fastapi import APIRouter, HTTPException
from backend.database import users_collection
from backend.auth import hash_password, verify_password, create_jwt
from backend.models import User
from pydantic import BaseModel

router = APIRouter()

@router.post("/register")
def register(user: User):
    """ Register a new user """
    
    # Check if an admin already exists
    if user.role == "A" and users_collection.find_one({"role": "A"}):
        raise HTTPException(status_code=400, detail="An admin already exists.")
    
    # Check if the user already exists
    if users_collection.find_one({"user_id": user.user_id}):
        raise HTTPException(status_code=400, detail="User already exists")
    
    user.password = hash_password(user.password)
    users_collection.insert_one(user.dict()) # Insert the user into the database
    return {"message": "User registered successfully"}

# Define the login request model
class LoginRequest(BaseModel):
    user_id: str
    password: str

@router.post("/login")
def login(user: LoginRequest):
    """ Login a user """
    db_user = users_collection.find_one({"user_id": user.user_id})
    # Check if the user exists and the password is correct
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = db_user["role"]
    token = create_jwt(user.user_id, role)
    print(f"Generated Token: {token}")
    return {"token": token} # Return the token generated from the user_id and role
