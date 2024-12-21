from fastapi import FastAPI
from Prompt_genrator import prompt_gen
from story_generation import gemini_story_gen_format
from playHT_TTS import playHT_AI_voice
from image_generater import image_generater
from video_generation import video_gen
app = FastAPI()
app.include_router(prompt_gen)
app.include_router(gemini_story_gen_format)
app.include_router(playHT_AI_voice)
app.include_router(image_generater)
app.include_router(video_gen)

