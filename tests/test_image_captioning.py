import unittest
from backend.steps.image_captioning import image_captioning

class TestImageCaptioning(unittest.TestCase):
    def test_caption_generation(self):
        test_image = r"tests\utils\test.jpg"  # Assicurati di avere un'immagine di test
        description = image_captioning(test_image)

        self.assertIsInstance(description, str)
        self.assertGreater(len(description), 0, "La descrizione generata è vuota!")

if __name__ == "__main__":
    unittest.main()
