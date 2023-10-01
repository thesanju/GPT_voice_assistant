import os
import openai
import requests
import io
from pydub import AudioSegment
from pydub.playback import play
from decouple import config  # Import the config function

# Load API keys from environment variables using config
openai.api_key = config('OPENAI_API_KEY')
ELEVEN_LABS_API_KEY = config('ELEVEN_LABS_API_KEY')

ELEVEN_LABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/piTKgcLEGmPE4e6mEKli"

def text_to_speech(text):
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(ELEVEN_LABS_API_URL, json=data, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        print("Error in Eleven Labs API response:", response.status_code)
        return None

def chat_with_gpt(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You funny sarcastic alien from mars and you should answer with 10 words each time."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message["content"]

while True:
    print("Please ask your question (or type 'exit' to quit):")
    user_input = input()

    if user_input.lower() == "exit":
        break

    gpt_response = chat_with_gpt(user_input)

    gpt_audio = text_to_speech(gpt_response)

    if gpt_audio is not None:
        audio = AudioSegment.from_file(io.BytesIO(gpt_audio), format="mp3")
        play(audio)
