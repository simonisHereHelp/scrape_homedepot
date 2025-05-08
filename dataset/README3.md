# Examplary Parse and Synthicating Prompts

# Load the small-apartment-ideas.md content
apartment_path = "/mnt/data/small-apartment-ideas.md"
content = Path(apartment_path).read_text(encoding="utf-8")

# Use title for SOP keyword
keyword = "Small Apartment Ideas"

# Parse content into valid sections
sections = re.split(r"##+\s*", content)[1:]
valid_sections = [s.strip() for s in sections if s.strip()]

# Initialize training entries
entries_apartment = []
step_count = 1

for section in valid_sections:
    title, bullets = extract_title_and_bullets(section)
    if not title:
        continue
    assistant_text = f"Step {step_count}: {title}\n" + "\n".join(f"- {b}" for b in bullets)
    entries_apartment.append({
        "system": system_prompt,
        "user": f"What is Step {step_count} for {keyword}?",
        "assistant": assistant_text
    })
    entries_apartment.append({
        "system": system_prompt,
        "user": f"I’ve completed Step {step_count - 1}. What’s next?",
        "assistant": assistant_text
    } if step_count > 1 else {
        "system": system_prompt,
        "user": f"How do I begin {keyword}?",
        "assistant": assistant_text
    })
    step_count += 1

# Add synthetic glossary entries
apartment_terms = {
    "multipurpose furniture": "Multipurpose furniture refers to pieces that serve more than one function, such as a sofa bed or an ottoman with storage.",
    "floating shelves": "Floating shelves are mounted directly to the wall without visible brackets, ideal for saving floor space.",
    "light-reflecting surfaces": "These are materials like mirrors or glossy finishes that help make small spaces feel larger by bouncing light around.",
    "zoning": "Zoning is a design strategy that divides a small space into functional areas, such as work, dining, and relaxation zones."
}
for term, definition in apartment_terms.items():
    entries_apartment.append({
        "system": system_prompt,
        "user": f"What does \"{term}\" mean?",
        "assistant": definition
    })

# Limit to 8–12 entries max for this file (select first N entries evenly)
max_entries = 12
selected_apartment_entries = entries_apartment[:max_entries]

# Append to STEP5.jsonl
step5_path = "/mnt/data/STEP5.jsonl"
with open(step5_path, "a", encoding="utf-8") as f:
    for entry in selected_apartment_entries:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

len(selected_apartment_entries)

---------------

# Load the small-apartment-ideas.md content
apartment_path = "/mnt/data/small-apartment-ideas.md"
content = Path(apartment_path).read_text(encoding="utf-8")

# Use title for SOP keyword
keyword = "Small Apartment Ideas"

# Parse content into valid sections
sections = re.split(r"##+\s*", content)[1:]
valid_sections = [s.strip() for s in sections if s.strip()]

# Initialize training entries
entries_apartment = []
step_count = 1

for section in valid_sections:
    title, bullets = extract_title_and_bullets(section)
    if not title:
        continue
    assistant_text = f"Step {step_count}: {title}\n" + "\n".join(f"- {b}" for b in bullets)
    entries_apartment.append({
        "system": system_prompt,
        "user": f"What is Step {step_count} for {keyword}?",
        "assistant": assistant_text
    })
    entries_apartment.append({
        "system": system_prompt,
        "user": f"I’ve completed Step {step_count - 1}. What’s next?",
        "assistant": assistant_text
    } if step_count > 1 else {
        "system": system_prompt,
        "user": f"How do I begin {keyword}?",
        "assistant": assistant_text
    })
    step_count += 1

# Add synthetic glossary entries
apartment_terms = {
    "multipurpose furniture": "Multipurpose furniture refers to pieces that serve more than one function, such as a sofa bed or an ottoman with storage.",
    "floating shelves": "Floating shelves are mounted directly to the wall without visible brackets, ideal for saving floor space.",
    "light-reflecting surfaces": "These are materials like mirrors or glossy finishes that help make small spaces feel larger by bouncing light around.",
    "zoning": "Zoning is a design strategy that divides a small space into functional areas, such as work, dining, and relaxation zones."
}
for term, definition in apartment_terms.items():
    entries_apartment.append({
        "system": system_prompt,
        "user": f"What does \"{term}\" mean?",
        "assistant": definition
    })

# Limit to 8–12 entries max for this file (select first N entries evenly)
max_entries = 12
selected_apartment_entries = entries_apartment[:max_entries]

# Append to STEP5.jsonl
step5_path = "/mnt/data/STEP5.jsonl"
with open(step5_path, "a", encoding="utf-8") as f:
    for entry in selected_apartment_entries:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

len(selected_apartment_entries)

----------------
