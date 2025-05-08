import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import time

# === Config ===
base_model_path = "models/llama3-3b-instruct"
lora_adapter_path = "models/llama3-diy3b-step1"

# === Load tokenizer and model at startup ===
print("🔧 Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

print("🔧 Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    device_map="auto",
    trust_remote_code=True,
    quantization_config=BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
)

print("🔧 Applying LoRA adapter...")
lora_model = PeftModel.from_pretrained(base_model, lora_adapter_path)
lora_model.eval()

# === FastAPI ===
app = FastAPI()

class InferenceInput(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

@app.post("/inference")
async def run_inference(input: InferenceInput):
    print("\n🟡 Awaiting inference prompt...")
    print(f"📨 Received inference query: {input.prompt}")

    inputs = tokenizer(input.prompt, return_tensors="pt").to("cuda")

    with torch.no_grad():
        start = time.time()
        output = lora_model.generate(
            **inputs,
            max_new_tokens=input.max_tokens,
            do_sample=True,
            temperature=input.temperature
        )
        duration = round(time.time() - start, 2)

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    print(f"✅ Response generated in {duration}s:\n{response}\n")

    return {
        "response": response,
        "elapsed_seconds": duration
    }
