import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from datasets import Dataset

# === Load STEP_test.jsonl (with "prompt" and "completion") ===
test_path = "dataset/STEP_test.jsonl"
with open(test_path, "r", encoding="utf-8") as f:
    raw_entries = [json.loads(line.strip()) for line in f if line.strip()]
test_dataset = Dataset.from_list([
    {"prompt": x["prompt"], "completion": x["completion"]}
    for x in raw_entries
])

# === Load fine-tuned model ===
model_path = "models/llama3-STEP3b5"
tokenizer = AutoTokenizer.from_pretrained(model_path)
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

# === Use same model as judge ===
judge_model = model
judge_tokenizer = tokenizer

# === Build prompt for judgment ===
def build_judge_prompt(prompt, expected, predicted):
    return f"""You are an expert SOP evaluator. Your job is to judge how closely a predicted procedural instruction matches the expected one, given the same user prompt.

### Prompt:
{prompt}

### Expected Completion:
{expected}

### Predicted Completion:
{predicted}

Evaluate the predicted response on the following:
- Is it procedurally accurate?
- Does it cover the key steps mentioned in the expected?
- Is the language appropriate and instructional?

Respond ONLY with a score from 1 to 5, where:
- 5 = excellent match
- 3 = partial match with acceptable deviation
- 1 = poor or unrelated

### Score:
"""

# === Run predictions and scoring ===
results = []
with open("judge3b5.md", "w", encoding="utf-8") as md:
    for i, ex in enumerate(test_dataset):
        # Generate response from model
        input_ids = tokenizer(ex["prompt"], return_tensors="pt").to(model.device)
        output_ids = model.generate(**input_ids, max_new_tokens=150)
        predicted = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Build judge prompt and get score
        meta_prompt = build_judge_prompt(ex["prompt"], ex["completion"], predicted)
        judge_input = judge_tokenizer(meta_prompt, return_tensors="pt").to(judge_model.device)
        judge_output = judge_model.generate(**judge_input, max_new_tokens=20)
        judge_response = judge_tokenizer.decode(judge_output[0], skip_special_tokens=True)

        score = next((int(s) for s in reversed(judge_response) if s.isdigit()), None)

        # Write markdown output
        md.write(f"# Record {i} #\n")
        md.write(f"### User:\n{ex['prompt'].strip()}\n\n")
        md.write(f"### Dataset: \n{ex['completion'].strip()}\n")
        md.write(f"### Model: \n{predicted.strip()}\n\n")
        md.write(f"### LLM Judgement Score###\n- {score if score else 'N/A'}\n\n")

        print(f"[{i}] ✅ Score: {score}")

print("✅ Markdown report saved to judge3b5.md")
