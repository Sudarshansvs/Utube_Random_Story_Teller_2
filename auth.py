import google.generativeai as genai
from huggingface_hub import InferenceClient
from pyht.client import TTSOptions
from pyht import Client
import datetime
import json
import re 
import os
from dotenv import load_dotenv
load_dotenv()



def gemini_auth():
    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
    model = genai.GenerativeModel("gemini-1.5-flash")
    op = open("op_file.txt", "r")
    x= op.read()
    response = model.generate_content(str(x))
    response_list_n = re.split(r"\*\*Part \d+: (.*?)\*\*",response.text )
    return response_list_n

def Image_Prompt(SP):
    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(str(SP))
    return response.text




def pyht_auth():
    client = Client(
        user_id=os.getenv("PLAY_HT_USER_ID"),
        api_key=os.getenv("PLAY_HT_API_KEY"),
    )
    options = TTSOptions(voice="s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json")
    voice_engine = 'PlayDialog-http'
    return client, options, voice_engine


def image_gen():
    client = InferenceClient("black-forest-labs/FLUX.1-dev", token=os.getenv("H_API"))
    return client