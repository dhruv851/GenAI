from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # or "gpt-4" if you have access
    messages=[
        {"role": "system", "content": "You are an expert in writing maths problems and only and only maths related questions."},
        {"role": "user", "content": "hey can you help me to solve a +b whole square."}
    ]
)

print(response.choices[0].message.content)