# Multi-Step Fine-Tuning Plan #

https://github.com/brevdev/launchables/blob/main/llama3_finetune_inference.ipynb


## environments: HF and Transformer
(hf_requirements.txt)
!pip install -q -U bitsandbytes
!pip install -q -U git+https://github.com/huggingface/transformers.git
!pip install -q -U git+https://github.com/huggingface/peft.git
!pip install -q -U git+https://github.com/huggingface/accelerate.git
!pip install trl

!pip install -U huggingface_hub
huggingface-cli login (use token to login, )

```
(hf_download.py)
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="meta-llama/Meta-Llama-3.2-3B",
    local_dir="./models/llama3-3b-instruct",  # Match your current folder layout
    local_dir_use_symlinks=False
)
```

## training

🧪 hf_train_parquet.py and hf_lora_inference.py

--hf_download.py: downlaod the Llama model
--datasetn HF: scooterman/guanaco-llama3-1k
![alt text](image-3.png)

## Deployment (FastAPI)

uvicorn hf_lora_api:app --host 0.0.0.0 --port 8000

curl -X POST http://localhost:8000/inference \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What games would you recommend if I liked Undertale?"}'
