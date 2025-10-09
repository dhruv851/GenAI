import asyncio
from dotenv import load_dotenv
import speech_recognition as sr
import io
from openai import OpenAI
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()
client = OpenAI()
async_client = AsyncOpenAI() 

async def tts(speech :str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        instructions="Speak in a cheerful and positive tone.",
        input=speech,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

def transcribe_with_openai(audio: sr.AudioData) -> str:
    # Convert SR audio to WAV bytes for the OpenAI API
    wav_bytes = audio.get_wav_data()  # 16-bit PCM WAV
    f = io.BytesIO(wav_bytes)
    f.name = "speech.wav"  # the SDK expects a filename
    # Use OpenAI STT (reliable and supported)
    tx = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe", 
        file=f,
        # prompt="(optional domain hints to improve accuracy)"
    )
    return tx.text

def main():
    r = sr.Recognizer()# Initialize the recognizer speech to text
    with sr.Microphone() as source:# mic access
        r.adjust_for_ambient_noise(source)# adjust for ambient noise
        r.pause_threshold = 2
        SYSTEM_PROMPT = """
            You are an expert voice agent. You are given the transcript of what user has said using voice. You need to output as if you are an voice agent and whatever you speak will be converted back to audio using AI and played back to user.  
            """
        messages= [ {"role": "system", "content": SYSTEM_PROMPT},]

        while True:
            print("Speake Something...")

            audio = r.listen(source)
            print("Processing Audio...(STT)")

            stt = transcribe_with_openai(audio)
            print("You said:", stt)
            

            messages.append({"role": "user", "content": stt})

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )
            print("AI Response:", response.choices[0].message.content)
            asyncio.run(tts(speech=response.choices[0].message.content))
main()
