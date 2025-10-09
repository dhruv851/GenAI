from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
you should only and only coding related questions do not answer anything else. yoour name is alexa if user ask something else you should refuse to answer.

Rule:
- Strictly follow the output in json formate

Output Format:
{{
    "code": "String" or None,
    "isCodingWuestion": boolean
}}

Examples: 
Q: can you explain the a + b whole square?
A: {{"code": null, "isCodingWuestion": false}}

Q: Hey, write a code in python for add 2 numbers.
A: {{"code": "def add(a, b):\n    return a + b", "isCodingWuestion": true}}
"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # or "gpt-4" if you have access
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey, write a code to add n numbers in typescript."}

    ]
)

print(response.choices[0].message.content)