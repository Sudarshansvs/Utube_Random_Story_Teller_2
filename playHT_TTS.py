from pyht import Client
from dotenv import load_dotenv
from pyht.client import TTSOptions
import os
import datetime
import json
load_dotenv()
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

client = Client(
    user_id=os.getenv("PLAY_HT_USER_ID"),
    api_key=os.getenv("PLAY_HT_API_KEY"),
)
Story_to_read = open("output_story.json", "r")
story_listobj = [json.loads(i) for i in Story_to_read]
print(story_listobj[-1])
tittle_story = story_listobj[-1]
x = tittle_story["story_title"]
x= str.replace(x, " ", "_")
print("tittle_story : ", tittle_story)
options = TTSOptions(voice="s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json")
#Open a file to save the audio
Audio_file_name = f"{x}_{timestamp}.wav"
story = tittle_story["story"]
print("story : ", story)
filtered_tsory = []
for part in story:
    if ":" in part:
        filtered_tsory.append(part.split(":"))
# story_list = story.split(":")

print("filtered_tsory :", filtered_tsory)
speak = filtered_tsory[0][0]
print(Audio_file_name, ": Audio_file_name")
with open("audio/{}".format(Audio_file_name), "wb") as audio_file:
    for chunk in client.tts(speak, options, voice_engine = 'PlayDialog-http'):
        # Write the audio chunk to the file
        audio_file.write(chunk)

print("audio/{}".format(Audio_file_name))