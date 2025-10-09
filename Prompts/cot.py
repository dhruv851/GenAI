#Chain of thought Prompting
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
    you are an expert ai assitance in resoving user queries using chain of thought. you work on START,PLAN and output steps.
    you need to first PLAN what need to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly follow the output in json formate
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (that can be multiple times) and finally OUTPUT (which is going to the display the final answer to user).

    Output JSON Format:
    { "step": "START" or "PLAN" or "OUTPUT", "content": "string}

    Examples:
    START: Hey, Can you solve 2 + 4 * 4 / 2
    PLAN: { "step": "PLAN", "content": "seems like user is intrested in maths problrm."}
    PLAN: { "step": "PLAN", "content": "looking at the problem we should solve this using BODMAS method"}
    PLAN: { "step": "PLAN", "content": "Yes, the BODMAS is correct thing to be done here"}
    PLAN: { "step": "PLAN", "content": "first we need to do multiplication 4 * 4 = 16"}
    PLAN: { "step": "PLAN", "content": "then we need to do addition 2 + 16 = 18"}
    PLAN: { "step": "PLAN", "content": "finally we need to do division 18 / 2 = 9"}
    OUTPUT: { "step": "OUTPUT", "content": "9"}
"""

print("\n\n\n\n")

message_history = [
   {"role": "system", "content": SYSTEM_PROMPT}
]

user_query = input("👉🏻")
message_history.append({"role": "user", "content": user_query})

while True:
   response = client.chat.completions.create(
      model="gpt-3.5-turbo",  # or "gpt-4" if you have access
      response_format={"type": "json_object"},
      messages=message_history
   )
   raw_result = response.choices[0].message.content
   message_history.append({"role": "assistant", "content": raw_result})

   parsed_result = json.loads(raw_result)

   if parsed_result["step"] == "START":
      print("🔥",parsed_result.get("content"))
      continue
   if parsed_result["step"] == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue
   if parsed_result["step"] == "OUTPUT":
        print("💡", parsed_result.get("content"))
        break

print("\n\n\n\n")
