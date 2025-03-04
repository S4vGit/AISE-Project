import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# Carica il tokenizer e il modello
model_name = "gpt2-medium"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Aggiungi un token di padding al tokenizer
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model.resize_token_embeddings(len(tokenizer))

# Carica il dataset CSV
df = pd.read_csv('Fake.csv')
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
test_size = int(len(df) * 0.1)
train_df = df[:-test_size]
test_df = df[-test_size:]

# Converti i DataFrame di pandas in un Dataset Hugging Face
train_dataset = Dataset.from_pandas(train_df[['text']])
test_dataset = Dataset.from_pandas(test_df[['text']])

# Tokenizzazione
def tokenize_function(examples):
    inputs = tokenizer(examples['text'], truncation=True, padding="max_length", max_length=150)
    inputs['labels'] = inputs['input_ids'].copy()
    return inputs

tokenized_train_dataset = train_dataset.map(tokenize_function, batched=True)
tokenized_test_dataset = test_dataset.map(tokenize_function, batched=True)

# Imposta i parametri di training
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",  # Usa eval_strategy invece di evaluation_strategy
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Crea un Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_test_dataset,  # Dataset di test per la valutazione
)

# Avvia il fine-tuning
trainer.train()

# Valuta il modello sul test set
eval_results = trainer.evaluate()
print("Risultati della valutazione:")
for key, value in eval_results.items():
    print(f"{key}: {value}")

# Funzione per generare fake news da descrizioni di test
def generate_fake_news(description):
    prompt = f"Create a fake news article based on this description: {description}"
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(inputs, max_length=150, num_return_sequences=1,
                            do_sample=True, top_k=50, top_p=0.95, temperature=0.7)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Esempi di descrizioni per il testing
test_samples = [
    "a man holding a red umbrella in a park",
    "a woman cooking in a kitchen with a cat",
    "people gathered around a table at a restaurant",
]

# Esegui il test di generazione
for description in test_samples:
    fake_news = generate_fake_news(description)
    print(f"Descrizione: {description}")
    print(f"Fake News Generata: {fake_news}\n")

# Salva il modello fine-tuned
model.save_pretrained("./fine_tuned_gpt2")
tokenizer.save_pretrained("./fine_tuned_gpt2")
