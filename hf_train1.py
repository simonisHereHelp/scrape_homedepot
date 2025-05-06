# train_meta.py (Meta-based training script without Hugging Face Hub or wandb)

import json
import yaml
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, TrainerCallback, BitsAndBytesConfig
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch
import os


# ✅ CUDA check and device setup
if not torch.cuda.is_available():
    raise EnvironmentError("CUDA is not available. Please ensure a compatible GPU and drivers are installed.")

device_name = torch.cuda.get_device_name(0)
print(f"✅ CUDA available: True | Using device: {device_name}")


# Hardcoded configuration
model_path = "./models/llama3-3b-instruct"
data_path = "./train_data1.jsonl"
output_path = "./models/llama3-diy3b-step1"

# Load tokenizer using AutoTokenizer (no need for tokenizer_file logic)
tokenizer = AutoTokenizer.from_pretrained(
    model_path,
    padding_side="right",
    truncation_side="right",
    use_fast=True
)
tokenizer.pad_token = "<|endoftext|>"

# Load dataset (hardcoded path)
print("📦 Loading dataset from:", data_path)
dataset = load_dataset("json", data_files=data_path)['train']
print("✅ Dataset loaded with", len(dataset), "samples")

def format_messages(example):
    text = ""
    for msg in example["messages"]:
        role = msg["role"]
        content = msg["content"]
        text += f"<|{role}|> {content}\n"
    example["text"] = text.strip()
    return example

dataset = dataset.map(format_messages)

# Load model directly from Meta-downloaded files
print("📥 Loading model from:", model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    config=os.path.join(model_path, "params.json"),
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True
)
model.resize_token_embeddings(len(tokenizer))

# Prepare LoRA model
model = prepare_model_for_kbit_training(model)
peft_config = LoraConfig(task_type="CAUSAL_LM", r=8, lora_alpha=32, lora_dropout=0.05)
model = get_peft_model(model, peft_config)

class CustomLoggingCallback(TrainerCallback):
    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % 10 == 0:
            print(f"📊 Step {state.global_step}: loss = {state.log_history[-1].get('loss', 'N/A')}")

# Training arguments
training_arguments = TrainingArguments(
    output_dir=output_path,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    num_train_epochs=3,
    logging_steps=1,
    save_steps=50,
    save_total_limit=2,
    fp16=True,
    optim="adamw_torch",
    report_to="none",
    warmup_steps=50,
    lr_scheduler_type="linear",
    logging_dir=os.path.join(output_path, "logs"),
    disable_tqdm=False
)


# Trainer with data collator for tokenizing text field
trainer = Trainer(
    model=model,
    train_dataset=dataset,
    args=training_arguments,
    tokenizer=tokenizer,
    callbacks=[CustomLoggingCallback()],
    data_collator=lambda data: tokenizer(
        [ex["text"] for ex in data],
        padding=True,
        truncation=True,
        return_tensors="pt"
    )
)

print("🚀 Starting training...")
trainer.train()

# Save the trained model
print("💾 Saving model to:", output_path)
trainer.model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)
print("✅ Training completed successfully")