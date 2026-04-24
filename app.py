from fastapi import FastAPI
from pydantic import BaseModel
from vllm import LLM, SamplingParams

app = FastAPI()

# Load model once (IMPORTANT for serverless performance)
llm = LLM(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    trust_remote_code=True
)

class Request(BaseModel):
    prompt: str
    max_tokens: int = 200
    temperature: float = 0.7

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/generate")
def generate(req: Request):
    sampling_params = SamplingParams(
        temperature=req.temperature,
        max_tokens=req.max_tokens
    )

    outputs = llm.generate([req.prompt], sampling_params)

    text = outputs[0].outputs[0].text

    return {
        "response": text
    }