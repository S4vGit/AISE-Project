from transformers import GPT2LMHeadModel, GPT2Tokenizer
from zenml import step
from typing_extensions import Annotated

# Upload fine-tuned GPT-2 model and tokenizer
model_name = "backend/steps/fine_tuned_gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

@step
def text_generation(description: str) -> Annotated[str, "Fake news"]:
    """Generate a fake news based on an image description."""
    prompt = f"Create a fake news article based on this description: {description}"
    inputs = tokenizer.encode(prompt, return_tensors='pt') # Tokenize the prompt

    # Generate the fake news
    output = model.generate(inputs, max_length=150, num_return_sequences=1,
                            do_sample=True, top_k=50, top_p=0.95, temperature=0.7
                            )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print(f"Fake news: {generated_text}")
    
    return generated_text