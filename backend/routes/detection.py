import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from backend.services.detection_service import detect_fake_news
from backend.database import fake_news_collection
from backend.models import FakeNews
from backend.auth import get_current_user

router = APIRouter()
UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the uploads folder if it doesn't exist

@router.post("/detect-fake-news")
async def detect_news(
    file: UploadFile = File(...), 
    current_user: dict = Depends(get_current_user) # Get the current user
):
    """ Detect fake news from an image """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")  # Check if the user is authenticated

    user_id = current_user["user_id"]  # Get the user

    # Generate the file path
    file_path = os.path.join(UPLOAD_FOLDER, f"{user_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        
    description, fake_news, fake_probability = detect_fake_news(file_path)
    
    # Create a new fake news document
    fake_news_document = FakeNews(
        image_path=file_path,
        user_id=user_id,
        description=description,
        generated_text=fake_news,
        fake_probability=fake_probability
    )
    fake_news_collection.insert_one(fake_news_document.dict()) # Insert the fake news into the database

    return {"description": description, "fake_news": fake_news, "fake_probability": fake_probability}
