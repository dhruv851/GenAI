#Chain of thought Prompting
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional
import os

load_dotenv()


client = OpenAI()


def run_command(cmd:str):
     result = os.system(cmd)
     return result
     
def fetch_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    else:
        print("Failed to fetch weather data.")
    return response.text

avialable_tools = {
    "get_weather": fetch_weather,
    "run_command": run_command
    }


SYSTEM_PROMPT = """
    you are an expert ai assitance in resoving user queries using chain of thought. you work on START,PLAN and output steps.
    you need to first PLAN what need to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the list of avilable tools.
    for every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Strictly follow the output in json formate
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (that can be multiple times) and finally OUTPUT (which is going to the display the final answer to user).

    Output JSON Format:
    Here is your output format:
    { "step": "START" or "PLAN" or "OUTPUT" or "TOOL", "content": "string", "input":"string"}

    Avilable Tools:
    - get_weather(city: str): Fetches the current weather for the specified city.
    - run_command(cmd: str): Takes system linux command as a string and execute the command on users system and returns the output.
    Example 1:
    START: Hey, Can you solve 2 + 4 * 4 / 2
    PLAN: { "step": "PLAN", "content": "seems like user is intrested in maths problrm."}
    PLAN: { "step": "PLAN", "content": "looking at the problem we should solve this using BODMAS method"}
    PLAN: { "step": "PLAN", "content": "Yes, the BODMAS is correct thing to be done here"}
    PLAN: { "step": "PLAN", "content": "first we need to do multiplication 4 * 4 = 16"}
    PLAN: { "step": "PLAN", "content": "then we need to do addition 2 + 16 = 18"}
    PLAN: { "step": "PLAN", "content": "finally we need to do division 18 / 2 = 9"}
    OUTPUT: { "step": "OUTPUT", "content": "9"}

    Example 2:
    START: What is the weather of surat.
    PLAN: { "step": "PLAN", "content": "seems like user is intrested in weather information of surat in india."}
    PLAN: { "step": "PLAN", "content": "lets see if we have any avialable tools from the list of avilable tools."}
    PLAN: { "step": "PLAN", "content": "Great, we have get_weather(city: str) tool for this query"}
    PLAN: { "step": "TOOL", "content": "I need to call get_weather tool for surat as input for city."}
    PLAN: { "step": "TOOL", "tool": "get_weather", "input": "surat"}
    PLAN: { "step": "OBSERVE", "tool": "get_weather", "output": "The temp of surat is cloudy with 20 C"}
    PLAN: { "step": "PLAN", "content": "Great, I got the weather info about surat"}
    PLAN: { "step": "PLAN", "content": "The weather in surat is cloudy with 20 C."}
    OUTPUT: { "step": "OUTPUT", "content": "The weather in surat is cloudy with 20 C."}
"""

print("\n\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step Example : START, PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call")
    input: Optional[str] = Field(None, description="The input params for the tool")


message_history = [
   {"role": "system", "content": SYSTEM_PROMPT}
]
while True:
    user_query = input("👉🏻")
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.parse(
            model="gpt-4o",  # or "gpt-4" if you have access
            response_format=MyOutputFormat,
            messages=message_history
        )
        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})

        parsed_result = response.choices[0].message.parsed


        if parsed_result.step == "START":
            print("🔥",parsed_result.content)
            continue
        
        if parsed_result.step == "TOOL":

            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            if not tool_to_call or tool_to_call not in avialable_tools:
                print(f"❌ Invalid or missing tool in response: {parsed_result}")
                continue
            print(f"🔧, {tool_to_call} ({tool_input})")
            tool_response = avialable_tools[tool_to_call](tool_input)
            print(f"🛠️ : {tool_to_call}({tool_input}) = {tool_response}")
            message_history.append({"role": "developer", "content": json.dumps({"step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response})})
            continue
        
        if parsed_result.step == "PLAN":
                print("🧠", parsed_result.content)
                continue
        
        if parsed_result.step == "OUTPUT":
                print("💡", parsed_result.content)
                break

print("\n\n\n\n")
