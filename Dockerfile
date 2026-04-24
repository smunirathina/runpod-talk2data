FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    python3-pip git && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Expose port
EXPOSE 8000

# Start server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]