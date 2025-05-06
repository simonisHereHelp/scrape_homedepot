import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

# === Prompt ===
prompt = "What games would you recommend if I liked Undertale?"

# === Paths ===
base_model_path = "models/llama3-3b-instruct"
lora_adapter_path = "models/llama3-diy3b-step1"

# === Load tokenizer ===
tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

# === Tokenize input once ===
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

# === Load base model ===
print("\n🚀 Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    device_map="auto",
    trust_remote_code=True,
    quantization_config=BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
)

# === Inference: base model ===
print("\n🧠 Running base model inference...")
with torch.no_grad():
    base_output = base_model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.7
    )
base_text = tokenizer.decode(base_output[0], skip_special_tokens=True)

print("\n🔹 Base Model Response:")
print(base_text)

# === Apply LoRA ===
print("\n🔧 Applying LoRA adapter...")
lora_model = PeftModel.from_pretrained(base_model, lora_adapter_path)

# === Inference: LoRA model ===
print("\n🧠 Running LoRA-adapted model inference...")
with torch.no_grad():
    lora_output = lora_model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.7
    )
lora_text = tokenizer.decode(lora_output[0], skip_special_tokens=True)

print("\n🔸 LoRA-Adapted Model Response:")
print(lora_text)
