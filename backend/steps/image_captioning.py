import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from zenml import step
from typing_extensions import Annotated


# Uploading BLIP-2 for Image Captioning
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)

@step
def image_captioning(image_path: str) -> Annotated[str, "Image description"]: 
    """Generate a text description of an image"""
    # Load the image
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        return f"Error during image loading: {str(e)}"
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        out = model.generate(**inputs) # Generate the caption
    
    caption = processor.decode(out[0], skip_special_tokens=True) # Decode the caption
    print(f"Generated description: {caption}")
    
    return caption