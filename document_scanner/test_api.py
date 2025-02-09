import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": "Test API call. Say hello."}],
        max_tokens=50,
    )
    print("API response:")
    print(response.choices[0].message.content)
except Exception as e:
    print("Error calling OpenAI API:")
    print(e)
