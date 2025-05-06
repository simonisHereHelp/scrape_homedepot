import os
import torch
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    TrainerCallback
)
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer

# == CUDA memory ==
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# === Paths ===
data_path = "dataset/train-00000-of-00001.parquet"
model_path = "models/llama3-3b-instruct"
output_path = "models/llama3-diy3b-step1"

# === CUDA Check ===
device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
print(f"✅ CUDA available: {torch.cuda.is_available()} | Using device: {device_name}")

# === Load Dataset ===
print("📦 Loading dataset from:", data_path)
df = pd.read_parquet(data_path)
dataset = Dataset.from_pandas(df)
print("✅ Dataset loaded with", len(dataset), "samples")

# === Load Tokenizer & Model ===
tokenizer = AutoTokenizer.from_pretrained(model_path, add_bos_token=True, add_eos_token=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",
    trust_remote_code=True,
    quantization_config=BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
)

# === Apply LoRA === 
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)

# === Training Args ===
training_args = TrainingArguments(
    output_dir=output_path,
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1,
    optim="paged_adamw_32bit",
    save_steps=100,
    logging_steps=5,
    learning_rate=2e-4,
    weight_decay=0.001,
    bf16=True,
    max_grad_norm=0.3,
    max_steps=5,
    warmup_ratio=0.03,
    group_by_length=True,
    report_to="none"
)

# === Logging Callback ===
class CustomLoggingCallback(TrainerCallback):
    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % 10 == 0 and state.log_history:
            last_log = state.log_history[-1]
            print(f"📊 Step {state.global_step}: loss = {last_log.get('loss', 'N/A')}")

# === Trainer ===     tokenizer=tokenizer (removed)
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    callbacks=[CustomLoggingCallback()]
)

# === Train ===
print("🚀 Starting fine-tuning...")
trainer.train()
print("✅ Training complete. Model saved to:", output_path)
