import os
from openai import OpenAI

# load OPENAI_API_KEY
top_p = 1
temperature = 0.4
max_tokens = 100
model_name = 'gpt-3.5-turbo'
openai_api_key_path = '/home/loc/Documents/OPENAI_API_KEY.txt'

with open(openai_api_key_path) as f:
    OPENAI_API_KEY = f.read().strip()
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

client = OpenAI()

query = 'Hello!'

responses = client.chat.completions.create(
            model = model_name,
            messages = [{'role':'user','content':query}],
            max_tokens = max_tokens,
            temperature = temperature,
            top_p = top_p
            )

print(responses.choices[0].message.content)