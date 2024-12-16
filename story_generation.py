import json
from fastapi import APIRouter
from auth import gemini_auth
import os
#http://localhost:8000/gemini_story_genAnd_format/gemini_story_genAnd_format
gemini_story_gen_format = APIRouter(
    prefix=('/gemini_story_genAnd_format'),
    tags = ['gemini_story_genAnd_format']
)

@gemini_story_gen_format.get('/gemini_story_genAnd_format')
def gemini_story_genAnd_format():
    response_list_n = gemini_auth()
    response_list = [i.strip() if i[-1] == "\n" else i for i in response_list_n[1:]]
    story_title = response_list[0]
    f_p = ":".join(response_list[0:2])
    first_part = ":".join(response_list[0:2])
    second_part =":".join(response_list[2:4])
    third_part = ":".join(response_list[4:])
    story_op = open("output_story.json","a+")
    {story_title: [first_part, second_part, third_part]}
    json_story = {"story_title":story_title, "story" :[first_part, second_part, third_part]}
    story_op.write(json.dumps(json_story))
    story_op.write("\n")
    return response_list_n, json_story, "Story written in format in the file : output_story.json"
