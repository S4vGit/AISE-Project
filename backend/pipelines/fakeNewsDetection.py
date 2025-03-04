import sys, os
from zenml.pipelines import pipeline
from zenml.logger import get_logger
from backend.steps import (text_generation, fake_news_detector, image_captioning)

# Add the main folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
logger = get_logger(__name__)

@pipeline(enable_cache=False)
def fake_news_pipeline_det(image_path: str):
    """Pipeline to detect fake news from text generated from image captioning"""
    description = image_captioning(image_path)
    generated_text = text_generation(description)
    fake_probability = fake_news_detector(generated_text)
    return description, generated_text, fake_probability
    
