from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = "you should only and only coding related questions do not answer anything else. yoour name is alexa if user ask something else you should refuse to answer."

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # or "gpt-4" if you have access
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "hi can you write python code for translation."}
    ]
)

print(response.choices[0].message.content)