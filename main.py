import os
import openai
import requests
import io
from pydub import AudioSegment
from pydub.playback import play
from decouple import config
import speech_recognition as sr

openai.api_key = config('OPENAI_API_KEY')
ELEVEN_LABS_API_KEY = config('ELEVEN_LABS_API_KEY')
ELEVEN_LABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/piTKgcLEGmPE4e6mEKli/stream"

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
    response = requests.post(ELEVEN_LABS_API_URL, json=data, headers=headers, stream=True)

    if response.status_code == 200:
        return response.content
    else:
        return None

def chat_with_gpt(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant, answer questions under 20 words."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message["content"]

recognizer = sr.Recognizer()
print("AI: Hello! I'm here to help. You can start the conversation. Say 'exit' to end.")

while True:
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

    try:
        user_input = recognizer.recognize_google(audio)
        print("You:", user_input)

        if user_input.lower() == "exit":
            print("AI: Goodbye!")
            break

        gpt_response = chat_with_gpt(user_input)
        print("AI:", gpt_response)

        gpt_audio = text_to_speech(gpt_response)

        if gpt_audio is not None:
            audio = AudioSegment.from_file(io.BytesIO(gpt_audio), format="mp3")
            play(audio)
    except sr.WaitTimeoutError:
        print("AI: I'm waiting for your question. Please speak within 3 seconds.")
    except sr.UnknownValueError:
        print("AI: Sorry, I couldn't understand your speech. Please speak clearly.")
    except sr.RequestError as e:
        print("AI: There was an error in recognizing your speech; {0}".format(e))
