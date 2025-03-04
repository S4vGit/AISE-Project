from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    role: str
    user_id: str
    password: str

class FakeNews(BaseModel):
    image_path: str
    user_id: str
    description: str
    generated_text: str
    fake_probability: Optional[str]
