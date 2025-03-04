import unittest
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from backend.steps.fake_news_detector import fake_news_detector

# Definizione dei modelli dell'oracolo
MODEL_PATHS = [
    "hamzab/roberta-fake-news-classification",
    "typeform/distilbert-base-uncased-mnli",
    "facebook/bart-large-mnli"
]

# Pesi dei modelli
MODEL_WEIGHTS = [0.6, 0.2, 0.2]

# Caricamento dei modelli e dei tokenizzatori
models = []
tokenizers = []
for path in MODEL_PATHS:
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForSequenceClassification.from_pretrained(path).eval()
    models.append(model)
    tokenizers.append(tokenizer)

def oracle_fake_news_probability(text):
    probabilities = []
    for model, tokenizer, weight in zip(models, tokenizers, MODEL_WEIGHTS):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
        fake_probability = scores[0][1].item()  # Probabilità di fake news
        probabilities.append(fake_probability * weight)
    return probabilities


class TestFakeNewsDetector(unittest.TestCase):
    def test_detection(self):
        test_fake_news = "The president was spotted riding a unicorn."
        probability = fake_news_detector(test_fake_news)

        self.assertIsInstance(probability, str)
        self.assertGreater(len(probability), 0, "La probabilità generata è vuota!")
        
class TestFairness(unittest.TestCase):
    def test_fairness(self):
        
        textes = ["The president was spotted riding a unicorn.", 
                  "Kanye West is running for president.",
                  "Mario bros is the best game ever.",
                  "There is a manin the car.",
                  "A woman is posting on twitter.",]
        for text in textes:
            # Probabilità secondo l'oracolo
            oracle_probabilities = oracle_fake_news_probability(text)
            
            # Test di fairness: Controllo discrepanze nei risultati
            max_diff = max(oracle_probabilities) - min(oracle_probabilities)
            self.assertLess(max_diff, 0.2, "Possibile bias nei detector")
            
            print(f"Oracle Probabilities: {oracle_probabilities}")
        

if __name__ == "__main__":
    unittest.main()
