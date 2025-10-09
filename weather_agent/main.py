from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

client = OpenAI()

def fetch_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    else:
        print("Failed to fetch weather data.")
    return response.text

def main():
    user_query = input("> ")
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "user", "content": user_query}
        ]
    )
    print("Response:", response.choices[0].message.content)


main()

