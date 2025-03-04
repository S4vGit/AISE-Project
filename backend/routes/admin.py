import os, shutil
from fastapi import APIRouter
from backend.database import users_collection, fake_news_collection
from typing import List, Dict

UPLOAD_FOLDER = "backend/uploads"
router = APIRouter()

@router.get("/overview", response_model=List[Dict])
def get_all_fake_news():
    """ Get all fake news from the database"""
    fake_news = list(fake_news_collection.find({}, {"_id": 0}))  # Retrieve all fake news from the database
    return fake_news

@router.delete("/clear-users")
async def clear_users():
    """ Clear all users from the database. """
    users_deleted = users_collection.delete_many({})
    return {
        "message": "All users deleted.",
        "users_deleted": users_deleted.deleted_count
    }

@router.delete("/clear-fake-news")
async def clear_fake_news():
    """ Clear all fake news from the database """
    fake_news_deleted = fake_news_collection.delete_many({})
    
    # Delete all uploaded images
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)  # Delete the uploads folder
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Recreate the uploads folder

    return {
        "message": "All fake news deleted.",
        "fake_news_deleted": fake_news_deleted.deleted_count,
        "uploads_cleared": True
    }