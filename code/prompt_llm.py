import transformers
import torch
from huggingface_hub import InferenceClient

# # model_id = "meta-llama/Meta-Llama-3-8B"
model_id = "/home/hatch5o6/nobackup/archive/huggingface/models/Meta-Llama-3-8B"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16}, 
    device='cuda'
)

prompt = "Hello. Who are you?"
print("PROMPT:")
print(prompt)
response = pipeline(prompt)
print("\nRESPONSE:")
print(response)