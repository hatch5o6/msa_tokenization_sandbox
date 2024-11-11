import argparse
import transformers
import torch
from huggingface_hub import InferenceClient
from tqdm import tqdm
import json

access_token = "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"
system_prompt = """You are an expert linguist and morphologian with export knowledge of word roots and structure."""
user_prompt_template = """Examine the following word in tripple backticks `````` and generate the root of the word:
Think carefully about each word, considering the following:
    - Think about what the base form of the word is. It may require removing afixes, adjust spelling, and chaning the stem.
    - If it is a compound word, generate the multiple roots deliminated by a single whitespace.

EXAMPLE 1:
establishment
OUTPUT:
establish

EXAMPLE 2:
reflects
OUTPUT:
reflect

EXAMPLE 3:
greenhouse
OUTPUT:
green house

EXAMPLE 4:
housing
OUTPUT:
house

EXAMPLE 5:
sung
OUTPUT:
sing


Now, generate only the root of the following word without explanations:
```{word}```
"""

def prompt_llm(
    words,
    model_id,
    LIMIT=None
):
    pipeline = transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16}, 
        device='cuda'
    )

    results = []
    for word in words:
        user_prompt = user_prompt_template.replace("{word}", word)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = pipeline(
            messages,
            max_new_tokens=1000
        )

        response = response[0]["generated_text"][-1]["content"].strip()
        print(f"'{word}': '{response}'")
        results.append(response)

    return results


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--words", "-w", required=True)
    parser.add_argument("--model", "-m", default="meta-llama/Llama-3.1-8B-Instruct")
    parser.add_argument("--LIMIT", type=int, default=None)
    parser.add_argument("--out", "-o", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    with open(args.words) as inf:
        words = inf.read().split()
    results = prompt_llm(
        words=words,
        model_id=args.model,
        LIMIT=args.LIMIT
    )

    with open(args.out, 'w') as outf:
        for i in range(len(words)):
            word = words[i]
            result = results[i]
            outf.write(f"'{word}': '{result}'\n")