#write a story in the genres of Fantacy+ Cyberpunk, theme coming of age + crime, atmosphere Humorous + Scary, include the charecters in India and Japan with names  Riya,Vihaan, and Ayaka, Ryo in 300 lines with proper ending. and divide the story to 3 parts each with equal length and suspense at the end of each part
import os
import json
import random
from fastapi import APIRouter
#http://localhost:8000/prompt_genertor/prompt_genertor
prompt_gen = APIRouter(
    prefix=('/prompt_genertor'),
    tags = ['prompt_genertor']
)


@prompt_gen.get('/prompt_genertor')
async def prompt_generator():
    input_country_list = ["India","Japan", "United States", "United Kingdom", "China"]
    input=open("story_json.json","r")
    Story_json = json.load(input)
    s1 = random.choice(input_country_list)
    s2 = random.choice(input_country_list)
    while s1==s2:
        s2= random.choice(input_country_list)

    g = random.choice(Story_json["genres"])
    t = random.choice(Story_json["themes"])
    a = random.choice(Story_json["atmospheres"])
    n1 = random.choice(Story_json["characters"][s1])
    n2 = random.choice(Story_json["characters"][s2])
    prompt_gven = f"write a thriller story in the genres of {g},with theme {t},atmosphere {a}, include the charecters in {s1, s2} with names {n1} and {n2} in 40 words with proper ending. and divide the story to 3 parts each with equal length and suspense at the end of each part, include tittle for each part"
    output_prompt = "op_file.txt"
    with open ("op_file.txt" , "w")as op:
        op.write(prompt_gven)
    return prompt_gven,"data written to file op_file.txt"