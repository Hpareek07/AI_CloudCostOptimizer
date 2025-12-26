import os
#
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_KEY,
)

def call_llm(prompt):
    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct:novita",
        response_format={"type": "json_object"},
        messages= prompt,
        temperature=0.1,
    )

    return completion.choices[0].message

