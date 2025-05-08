import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# === Load fine-tuned model ===
model_path = "models/llama3-STEP3b5"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",
    trust_remote_code=True,
    quantization_config=BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
)

# === Example prompt (simulate the style used in training) ===
user_prompt = """You are a procedural assistant trained to guide users through technical SOPs step-by-step with clarity and context.

### User:
I've completed Step 7. What's next?

### Assistant:"""

# === Tokenize and generate ===
input_ids = tokenizer(user_prompt, return_tensors="pt").to(model.device)
output = model.generate(**input_ids, max_new_tokens=150, do_sample=True, temperature=0.7)

# === Decode ===
response = tokenizer.decode(output[0], skip_special_tokens=True)
print("\n📋 Model Response:\n")
print(response)
