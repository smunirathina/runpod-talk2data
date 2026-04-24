import runpod
import subprocess
import time
import requests
import os

MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"

# ----------------------------------------
# Start vLLM OpenAI-compatible server
# ----------------------------------------
def start_vllm():
    cmd = [
        "python3", "-m", "vllm.entrypoints.openai.api_server",
        "--model", MODEL_NAME,
        "--host", "0.0.0.0",
        "--port", "8000",
        "--dtype", "half",
        "--max-model-len", "4096"
    ]

    return subprocess.Popen(cmd)


# ----------------------------------------
# Wait until server is ready
# ----------------------------------------
def wait_for_server():
    url = "http://localhost:8000/v1/models"

    for _ in range(60):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print("vLLM is ready")
                return
        except:
            pass
        time.sleep(2)

    raise RuntimeError("vLLM failed to start")


# ----------------------------------------
# RunPod handler (proxy to vLLM API)
# ----------------------------------------
def handler(event):
    data = event.get("input", {})
    prompt = data.get("prompt", "")
    max_tokens = data.get("max_tokens", 200)

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    response = requests.post(
        "http://localhost:8000/v1/chat/completions",
        json=payload
    )

    return response.json()


# ----------------------------------------
# Startup sequence
# ----------------------------------------
print("Starting vLLM server...")
vllm_process = start_vllm()

wait_for_server()

print("Starting RunPod handler...")
runpod.serverless.start({"handler": handler})
