from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",  # or
    messages=[
        {
            "role": "user", "content": [
                {"type": "text", "text": "Genrate a caption about this image in 50 words"},
                {"type": "image_url", "image_url": {"url": "https://images.pexels.com/photos/943096/pexels-photo-943096.jpeg"}}
            ]
        }
    ]
)

print("Response : ", response.choices[0].message.content)