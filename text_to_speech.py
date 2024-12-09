import json
import pyttsx3
from rsa.core import encrypt_int
# from transformers import pipeline
# summarizer = pipeline("summarization")




script_story_file = open("output_story.json", "r")
obj = [json.loads(i) for i in script_story_file]
stories = obj[-1]["story"][0].strip()
stories_list_words = stories.split(":")
# stories = obj[-1]["story"]
#story[0].first_part
# engine = pyttsx3.init()
print(stories_list_words)
# summary = summarizer(stories)[0]['summary_text']
# engine.say(summary)
# engine.runAndWait()
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 0.9)
for word in stories_list_words:
    engine.say(word)
    engine.runAndWait()



