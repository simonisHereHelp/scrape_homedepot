import os
import json
import torch
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

# === CUDA memory ===
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# === Paths ===
data_path = "dataset/STEP_train_clean.jsonl"
model_path = "models/llama3-3b-instruct"
output_path = "models/llama3-STEP3b5"

# === CUDA Check ===
device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
print(f"✅ CUDA available: {torch.cuda.is_available()} | Using device: {device_name}")

# === Load Training Set ===
print("📦 Loading dataset from:", data_path)
with open(data_path, "r", encoding="utf-8") as f:
    raw_entries = [json.loads(line) for line in f]

records = []
for ex in raw_entries:
    combined = f"{ex['prompt'].strip()}\n{ex['completion'].strip()}"
    records.append({"text": combined})

train_dataset = Dataset.from_list(records)
print("✅ Loaded training set with", len(train_dataset), "samples")

# === Load Tokenizer & Model ===
tokenizer = AutoTokenizer.from_pretrained(model_path, add_bos_token=True, add_eos_token=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.save_pretrained(output_path)

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
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1,
    optim="paged_adamw_32bit",
    save_steps=25,
    logging_steps=5,
    learning_rate=2e-4,
    weight_decay=0.001,
    bf16=True,
    max_grad_norm=0.3,
    max_steps=300,
    warmup_ratio=0.03,
    group_by_length=True,
    report_to="none"
)

# === Markdown Logger ===
class CustomLoggingCallback(TrainerCallback):
    def __init__(self, log_file="training_log3b5.md"):
        self.log_file = log_file
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("| Step | Loss |\n|------|------|\n")

    def on_step_end(self, args, state, control, **kwargs):
        if state.log_history:
            last_log = state.log_history[-1]
            step = state.global_step
            loss = last_log.get("loss", None)
            if loss is not None:
                print(f"📊 Step {step}: loss = {loss}")
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"| {step} | {loss:.4f} |\n")

# === Launch Training ===
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    callbacks=[CustomLoggingCallback()]
)

print("🚀 Starting training...")
trainer.train()
print("✅ Training complete. Saving model...")

model.save_pretrained(output_path)
print("✅ Model weights saved to:", output_path)
