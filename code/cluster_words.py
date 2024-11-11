import argparse
import transformers
import torch
from huggingface_hub import InferenceClient
from tqdm import tqdm
import json

access_token = "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"
system_prompt = """You are an expert linguist and morphologian with export knowledge of word roots and structure."""
user_prompt_template = """Examine the list of words and cluster them into word families where a word family is made of all words that contain the same root.
This includes inflections of the same word, such as 'read', 'reads' and 'reading', but also includes derivatives such as 'readable'.
Think carefully about each word and consider that some words may share a root but experience a stem change.
In the case of compound nouns, such as 'playground', we have two roots, and you should consider them as members of the familes of both roots.

Format the output as a list of lists, where each inner list contains all the words in a family.

For instance, consider the following list of words in triple backticks ``` ``` as an example input:
```
reflection
national
rang
greenhouse
reflect
house
ring
nation
housing
reflecting
rung
nationalize
green
reflects
```

You would output the following clusters based on their word families, formatted into a list of lists:
```
[
    ["reflect", "reflects", "reflecting", "reflection"],
    ["nation", "national", "nationalize"],
    ["house", "greenhouse", "housing"],
    ["green", "greenhouse"],
    ["ring", "rang", "rung"]
]
```

Notice that greenhouse is in two word families because it has two roots: "green" and "house". Make sure to do likewise when you encounter words with two or more roots.
Notice that "ring", "rang", and "rung" belong to the same word family even though they exhibit stem changes.

Now, review the following list of words and cluster them into word families. Make sure to put each and every word in a word family. Only output the list of lists without any explanations.
```
{list}
```
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

    word_list = "\n".join(words[:LIMIT])
    user_prompt = user_prompt_template.replace("{list}", word_list)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = pipeline(
        messages,
        max_new_tokens=1000
    )

    response = response[0]["generated_text"][-1]["content"]
    # response = json.dumps(response, ensure_ascii=False, indent=2)
    print(response)

    return response

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
    response = prompt_llm(
        words=words,
        model_id=args.model,
        LIMIT=args.LIMIT
    )

    with open(args.out, 'w') as outf:
        outf.write(response)