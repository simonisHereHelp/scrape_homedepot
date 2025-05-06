import os
import json
import re
import textwrap

input_dir = "diy_articles"
output_file = "train_data1.jsonl"
chunk_char_limit = 2500  # adjust based on token estimate

def clean_markdown(md_text):
    # Remove markdown-style links, keep just the visible text
    return re.sub(r'\[(.*?)\]\([^\)]*\)', r'\1', md_text)

def chunk_text(text, chunk_size):
    return textwrap.wrap(text, width=chunk_size, break_long_words=False, break_on_hyphens=False)

records = []

for filename in sorted(os.listdir(input_dir)):
    if not filename.endswith(".md"):
        continue
    with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as infile:
        lines = infile.readlines()
        title = ""
        body_lines = []
        for line in lines:
            if line.startswith("# ") and not title:
                title = line.strip("# ").strip()
            else:
                body_lines.append(line.strip())

        body = clean_markdown("\n".join(body_lines).strip())
        chunks = chunk_text(body, chunk_char_limit)

        for i, chunk in enumerate(chunks):
            records.append({
                "messages": [
                    {"role": "user", "content": f"Title: {title} (part {i+1})"},
                    {"role": "assistant", "content": chunk.strip()}
                ]
            })

with open(output_file, "w", encoding="utf-8") as outfile:
    for r in records:
        outfile.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"✅ Saved {len(records)} samples to {output_file} from '{input_dir}/'")
