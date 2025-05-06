# train_meta.py (Meta-based training script without Hugging Face Hub or wandb)

import json
import yaml
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch
import os

# Hardcoded configuration
model_path = "models/Mistral-7B-v0.1"
data_path = "./train_data1.jsonl"
output_path = "./models/mistral-diy7b-step1"

# Load tokenizer using AutoTokenizer (no need for tokenizer_file logic)
tokenizer = AutoTokenizer.from_pretrained(
    model_path,
    padding_side="right",
    truncation_side="right",
    use_fast=True
)
tokenizer.pad_token = "<|endoftext|>"

# Load dataset (hardcoded path)
dataset = load_dataset("json", data_files=data_path)['train']

# Load model directly from Meta-downloaded files
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    config=os.path.join(model_path, "config.json"),
    torch_dtype=torch.float16
)
model.resize_token_embeddings(len(tokenizer))

# Prepare LoRA model
model = prepare_model_for_kbit_training(model)
peft_config = LoraConfig(task_type="CAUSAL_LM", r=8, lora_alpha=32, lora_dropout=0.05)
model = get_peft_model(model, peft_config)

# Training arguments
training_arguments = TrainingArguments(
    output_dir=output_path,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    num_train_epochs=3,
    logging_steps=10,
    save_steps=50,
    save_total_limit=2,
    fp16=True,
    optim="adamw_torch",
    report_to="none",
    warmup_steps=50,
    lr_scheduler_type="linear"
)

# Trainer
trainer = Trainer(
    model=model,
    train_dataset=dataset,
    args=training_arguments,
    tokenizer=tokenizer
)

trainer.train()

# Save the trained model
trainer.model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)
