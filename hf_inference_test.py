import requests

# === FastAPI endpoint ===
url = "http://127.0.0.1:8000/inference"

# === Inference prompt ===
payload = {
    "prompt": "What games would you recommend if I liked Undertale?",
    "max_tokens": 100,
    "temperature": 0.7
}

# === Send POST request ===
print("🚀 Sending request to inference API...")
response = requests.post(url, json=payload)

# === Parse and display result ===
if response.status_code == 200:
    result = response.json()
    print("\n✅ Response received:")
    print("🧠 Output:", result["response"])
    print("⏱️ Time:", result["elapsed_seconds"], "seconds")
else:
    print("❌ Request failed:", response.status_code)
    print(response.text)
