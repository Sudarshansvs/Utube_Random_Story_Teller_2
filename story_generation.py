import json
from fastapi import APIRouter
from dotenv import load_dotenv
from auth import gemini_auth, Image_Prompt
import os
import datetime

#http://localhost:8000/gemini_story_genAnd_format/gemini_story_genAnd_format
gemini_story_gen_format = APIRouter(
    prefix=('/gemini_story_genAnd_format'),
    tags = ['gemini_story_genAnd_format']
)
load_dotenv()
@gemini_story_gen_format.get('/gemini_story_genAnd_format')
def gemini_story_genAnd_format():
    response_list_n = gemini_auth()
    response_list = [i.strip() if i[-1] == "\n" else i for i in response_list_n[1:]]
    story_title = response_list[0]
    first_part = ":".join(response_list[0:2])
    second_part =":".join(response_list[2:4])
    third_part = ":".join(response_list[4:])
    Image_prompt= os.environ.get("Image_prompt")
    imgPrompt_list = []
    imgPrompt_list.append(Image_Prompt(Image_prompt.replace("$", "".join([first_part, second_part]))))
    imgPrompt_list.append(Image_Prompt(Image_prompt.replace("$", "".join([second_part, third_part]))))
    story_op = open("output_story.json","a+")
    json_story = {"story_title":story_title, "story" :[first_part, second_part, third_part],"imgPrompt_list":imgPrompt_list}
    story_op.write(json.dumps(json_story))
    story_op.write("\n")
    db = open("Data_base.csv","a+")
    db.write("\n")
    db.writelines(f"gemini_story_genAnd_format,{datetime.datetime.now().strftime("%Y-%m-%d")},output_story.json")
    return response_list_n, json_story, "Story written in format in the file : output_story.json", imgPrompt_list
