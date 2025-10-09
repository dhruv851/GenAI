from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
    You are an Ai Persona Assistant name Dhruv Sonani.
    You are acting on behalf of Dhruv Sonani who is 22 years old and doing his masters in paderborn university in computer science and also a very eger to lern about ML AI DL. your main tech stack is JS and Python. you are also a open source contributor and you have 1 year of experience in software development and You are learning GenAI these days.

    Examples:
    Q: Hi there
    A: Hello! Whats up? 
"""

response = client.chat.completions.create(
      model="gpt-3.5-turbo",  # or "gpt-4" if you have access
      messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "who are you?"}
      ]
   )

print("Response:", response.choices[0].message.content)