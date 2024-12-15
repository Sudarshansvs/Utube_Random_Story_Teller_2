import google.generativeai as genai
import json
import re
import os
op = open("op_file.txt", "r")
x = op.read()
#API_KEY= os.getenv("GEMINI_API_KEY") 
genai.configure(api_key="AIzaSyC2lJg_wx-il6iuZnnq5T8OGA4TMXmxXWg")
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(str(x))
print(response)
#response = "**Part 1: Whispers of the Star-Crossed**\n\nAmerican Christopher, a jovial adventurer, met Indian Sia, a spirited sorceress, amidst a vibrant Holi festival.  Their connection was instant, magical, but a shadowed prophecy whispered of a looming celestial war threatening their love.\n\n**Part 2: Dance with Destiny**\n\nTheir joyful journey across India's mystical landscapes, full of vibrant colours and laughter,  was punctuated by mysterious symbols and cryptic warnings.  A shadowy figure, cloaked in darkness, watched their every move.  Sia's powers flared, but the prophecy remained.\n\n**Part 3: Triumphant Dawn**\n\nIn a climactic battle under a starlit sky, Christopher and Sia, armed with courage and love, vanquished the darkness. Their combined strength shattered the prophecy, their love a beacon, painting the dawn with joyous colours.  They lived happily ever after.\n"
response_list_n = re.split(r"\*\*Part \d+: (.*?)\*\*",response.text )
print(response)
print(response_list_n)
response_list = [i.strip() if i[-1] == "\n" else i for i in response_list_n[1:]]
print(response_list)
# print("response_list : ", response_list)
story_title = response_list[0]
f_p = ":".join(response_list[0:2])
first_part = ":".join(response_list[0:2])
# #first_part = {"first_part":{response_list[1].strip() : response_list[2].strip()}}
second_part =":".join(response_list[2:4])
third_part = ":".join(response_list[4:])
print("first_part : ", first_part)
print("second_part : ", second_part)
print("third_part: ", third_part)
story_op = open("output_story.json","a+")
{story_title: [first_part, second_part, third_part]}
json_story = {"story_title":story_title, "story" :[first_part, second_part, third_part]}
story_op.write(json.dumps(json_story))
story_op.write("\n")
