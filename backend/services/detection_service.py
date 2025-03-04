from backend.pipelines.fakeNewsDetection import fake_news_pipeline_det

def detect_fake_news(image_path: str):
    """Detect fake news from an image."""
    result = fake_news_pipeline_det(image_path) # Run the detection pipeline

    if result: # Check if the pipeline ran successfully
        image_captioning_step = result.steps.get("image_captioning")
        text_generation_step = result.steps.get("text_generation")
        fake_news_detector_step = result.steps.get("fake_news_detector")
        
        # Get the outputs from the steps
        description = image_captioning_step.outputs["Image description"][0].load()
        fake_news = text_generation_step.outputs["Fake news"][0].load()
        fake_probability = fake_news_detector_step.outputs["Fake probability"][0].load()
        
        return description, fake_news, fake_probability # Return the results
    else:
        return "", "", ""