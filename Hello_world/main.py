
# import google.generativeai as genai

# genai.configure(api_key="AIzaSyCCFpT4t8CS7Yal2sXTF3bvyzNfehs7BnU")

# model = genai.GenerativeModel("gemini-1.5-flash")
# chat = model.start_chat(history=[])
# response = chat.send_message("Explain to me how AI works")
# print(response.text)

# client = genai.client("api_key=AIzaSyCCFpT4t8CS7Yal2sXTF3bvyzNfehs7BnU")
# response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     messages=[
#         {"role": "user", "content": "Explain to me how AI in few works"}
#     ]
# )


# from google import genai

# # The client gets the API key from the environment variable `GEMINI_API_KEY`.
# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
# )
# print(response.text)


