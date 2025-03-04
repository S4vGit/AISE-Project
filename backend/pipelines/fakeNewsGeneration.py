import sys, os
from zenml.pipelines import pipeline
from zenml.logger import get_logger
from backend.steps import (text_generation, image_captioning)
from typing_extensions import Annotated

# Add the main folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
logger = get_logger(__name__)

@pipeline(enable_cache=False)
def fake_news_pipeline_gen(image_path: str) -> Annotated[tuple[str, str], "Description adn fake news"]: 
    """Pipeline to generate fake news from image captioning"""
    description = image_captioning(image_path)
    fake_news = text_generation(description)
    return description, fake_news
    