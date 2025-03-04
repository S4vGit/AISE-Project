import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from zenml import step
from typing_extensions import Annotated

# Defining oracle models
MODEL_PATHS = [
    "hamzab/roberta-fake-news-classification",
    "typeform/distilbert-base-uncased-mnli",
    "facebook/bart-large-mnli"
]

# Weighting the models
MODEL_WEIGHTS = [0.6, 0.2, 0.2]

# Loading models and tokenizers
models = []
tokenizers = []
for path in MODEL_PATHS:
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForSequenceClassification.from_pretrained(path).eval()
    models.append(model)
    tokenizers.append(tokenizer)

@step
def fake_news_detector(generated_text: str) -> Annotated[str, "Fake probability"]:
    """Classifies fake news using an ensemble of models with weighted probabilities."""
    # Loop through the models and calculate the fake probability
    probabilities = []
    for model, tokenizer, weight in zip(models, tokenizers, MODEL_WEIGHTS):
        inputs = tokenizer(generated_text, return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
        fake_probability = scores[0][1].item()  # Fake news probability
        print(fake_probability)
        probabilities.append(fake_probability * weight)
    
    # Calculate the weighted fake probability
    weighted_fake_probability = sum(probabilities)
    weighted_fake_probability = str(weighted_fake_probability)
    
    print(f"Fake probability: {weighted_fake_probability}")
    
    return weighted_fake_probability