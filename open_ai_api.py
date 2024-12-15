from dotenv import load_dotenv, find_dotenv
from typing import * 
from tempfile import NamedTemporaryFile
import os 
import openai
from pathlib import Path
import base64

# load_dotenv(find_dotenv)
# OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
Adio_file = "audio_output.mp3"

def ttscript(OPEN_AI_API_KEY):
    client = openai.OpenAI(api_key=OPEN_AI_API_KEY)

    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hi Alloy"
    )
    response.stream_to_file(Adio_file)
    


