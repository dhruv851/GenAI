from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional
import json
import requests
import os

load_dotenv()

client = OpenAI()


def fetch_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Failed to fetch weather data."


def run_command(cmd: str):
    return os.system(cmd)


available_tools = {
    "get_weather": fetch_weather,
    "run_command": run_command,
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
    { "step": "START" or "PLAN" or "OUTPUT" or "TOOL", "content": "string", "input":"string"}

    Avilable Tools:
    - get_weather(city: str): Fetches the current weather for the specified city.
    - run_command(cmd: str): Takes system linux command as a string and execute the command on users system and returns the output.

    Example:
    START: What is the weather of surat.
    PLAN: { "step": "PLAN", "content": "user wants weather info for surat."}
    PLAN: { "step": "TOOL", "tool": "get_weather", "input": "surat"}
    PLAN: { "step": "OBSERVE", "tool": "get_weather", "output": "The temp of surat is cloudy with 20 C"}
    OUTPUT: { "step": "OUTPUT", "content": "The weather in surat is cloudy with 20 C."}
"""


class OutputFormat(BaseModel):
    step: str = Field(..., description="START, PLAN, OUTPUT, TOOL, or OBSERVE")
    content: Optional[str] = Field(None)
    tool: Optional[str] = Field(None)
    input: Optional[str] = Field(None)


def run():
    message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_query = input("👉🏻 ")
        message_history.append({"role": "user", "content": user_query})

        while True:
            response = client.chat.completions.parse(
                model="gpt-4o",
                response_format=OutputFormat,
                messages=message_history,
            )
            raw_result = response.choices[0].message.content
            message_history.append({"role": "assistant", "content": raw_result})
            parsed = response.choices[0].message.parsed

            if parsed.step == "PLAN":
                print("🧠", parsed.content)
            elif parsed.step == "TOOL":
                tool_fn = available_tools.get(parsed.tool)
                if not tool_fn:
                    print(f"❌ Unknown tool: {parsed.tool}")
                    continue
                print(f"🔧 {parsed.tool}({parsed.input})")
                result = tool_fn(parsed.input)
                print(f"🛠️ Result: {result}")
                message_history.append({
                    "role": "developer",
                    "content": json.dumps({"step": "OBSERVE", "tool": parsed.tool, "input": parsed.input, "output": result}),
                })
            elif parsed.step == "OUTPUT":
                print("💡", parsed.content)
                break
