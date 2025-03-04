from backend.pipelines.fakeNewsGeneration import fake_news_pipeline_gen

def process_image(image_path: str): 
    """Process an image and generate a fake news article."""

    result = fake_news_pipeline_gen(image_path) # Run the generation pipeline
    
    if result: # Check if the pipeline ran successfully
        image_captioning_step = result.steps.get("image_captioning")
        text_generation_step = result.steps.get("text_generation")

        # Get the outputs from the steps
        description = image_captioning_step.outputs["Image description"][0].load()
        fake_news = text_generation_step.outputs["Fake news"][0].load()
        
        return description, fake_news # Return the results
    else:
        return "", ""
