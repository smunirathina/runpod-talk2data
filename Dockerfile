FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV HUGGING_FACE_HUB_TOKEN=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


WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 python3-pip git && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

# vLLM + RunPod SDK
RUN pip3 install vllm runpod

# Optional but recommended
RUN pip3 install transformers accelerate sentencepiece

COPY . .

# Start vLLM OpenAI-compatible server
CMD ["python3", "server.py"]
