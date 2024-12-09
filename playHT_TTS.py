# from pyht import Client, Format
# from dotenv import load_dotenv
from pyht.client import TTSOptions
import json
import asyncio
# # from playsound import playsound
# load_dotenv()
# op = open("audio_output.mp3", "wb+")
# client = Client(
#     user_id="IMbkwOvQK5fbYzJjGGyCNyfXjWr1",
#     api_key="ed26a325e15745a78dfb87cb65e9548b",
# )
#
# options = TTSOptions(voice="s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/male-cs/manifest.json",
#                      format=Format.FORMAT_MP3,
#                      sample_rate= 16000, speed=0.8)
# script_story_file = open("output_story.json", "r")
# obj = [json.loads(i) for i in script_story_file]
# stories = obj[-1]["story"][0].strip()
# stories_list_words = stories.split(" ")
# for chunk in client.stream_tts_input(stories_list_words, options):
#     op.write(chunk)
# #playsound('audio_output.mp3')
#

from pyht import AsyncClient
op = open("audio_output.mp3", "wb+")
client = AsyncClient(
    user_id="IMbkwOvQK5fbYzJjGGyCNyfXjWr1",
    api_key="",
)
script_story_file = open("output_story.json", "r")
obj = [json.loads(i) for i in script_story_file]
stories = obj[-1]["story"][0].strip()
stories_list_words = stories.split(" ")

options = TTSOptions(voice="s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json")
async def process_tts(client, options, op):
    async for chunk in client.tts("Hi, I'm Jennifer from Play. How can I help you today?", options):
        # do something with the audio chunk
        #print(type(chunk))
        op.write(chunk)

asyncio.run(process_tts(client, options, op))
print("written to : ", op)