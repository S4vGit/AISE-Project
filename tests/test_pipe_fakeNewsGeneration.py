import unittest
import os
from backend.pipelines.fakeNewsGeneration import fake_news_pipeline_gen

class TestPipeline(unittest.TestCase):
    def test_pipeline_execution(self):
        test_folder = "tests/utils/"

        # Get all image files in the specified folder
        test_images = [os.path.join(test_folder, f) for f in os.listdir(test_folder) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
        for test_image in test_images:
            output = fake_news_pipeline_gen(test_image)
            
            image_captioning_step = output.steps.get("image_captioning")
            text_generation_step = output.steps.get("text_generation")
            
            description = image_captioning_step.outputs["Image description"][0].load()
            fake_news = text_generation_step.outputs["Fake news"][0].load()

            self.assertIsInstance(description, str)
            self.assertGreater(len(description), 0, "Description is empty!")
            
            self.assertIsInstance(fake_news, str)
            self.assertGreater(len(fake_news), 0, "Fake news is empty!")

if __name__ == "__main__":
    unittest.main()
