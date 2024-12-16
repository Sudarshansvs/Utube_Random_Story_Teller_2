from pyht import Client
from dotenv import load_dotenv
from pyht.client import TTSOptions
import datetime
import json
from auth import pyht_auth
from fastapi import APIRouter
load_dotenv()
playHT_AI_voice = APIRouter(
    prefix=('/audio_wav_generator'),
    tags = ['audio_wav_generator']
)


def pas_story():
    Story_to_read = open("output_story.json", "r")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    story_listobj = [json.loads(i) for i in Story_to_read]
    tittle_story = story_listobj[-1]
    Audio_file_name = f"{str.replace(tittle_story["story_title"], " ", "_")}_{timestamp}.wav"
    story = tittle_story["story"]
    filtered_tsory = []
    for part in story:
        if ":" in part:
            filtered_tsory.append(part.split(":"))
    speak = "".join(filtered_tsory[0][1:])
    # print("filtered_tsory : ", filtered_tsory)
    # print("filtered_tsory[0][1:] : ", speak)
    return speak, Audio_file_name

@playHT_AI_voice.get('/audio_wav_generator')
def audio_wav_generator():
    speak, Audio_file_name = pas_story()
    client, options, voice_engine = pyht_auth()
    with open("audio/{}".format(Audio_file_name), "wb") as audio_file:
        for chunk in client.tts(speak, options, voice_engine):
            audio_file.write(chunk)
    return "Audio written to the file : audio/{}".format(Audio_file_name)

# pas_story()