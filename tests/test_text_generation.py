import unittest
from backend.steps.text_generation import text_generation

class TestTextGeneration(unittest.TestCase):
    def test_fake_news_generation(self):
        descriptions = ["The president was spotted riding a unicorn.", 
                  "",
                  "Mario bros is the best game ever.",
                  "There is a manin the car.",
                  "A dog is running in the park.",]
        
        for description in descriptions:
            fake_news = text_generation(description)

            self.assertIsInstance(fake_news, str)
            self.assertGreater(len(fake_news), 0, "La fake news generata è vuota!")

if __name__ == "__main__":
    unittest.main()
