import google.generativeai as genai
import json
import re
op = open("op_file.txt", "r")
x = op.read()
genai.configure(api_key="AIzaSyD52uM0jnpsAUFIEKlXaCRyw8Tz1zsVzf0")
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(str(x))
response_list_n = re.split(r"\*\*Part \d+: (.*?)\*\*",response.text )
response_list = [i.strip() if i[-1] == "\n" else i for i in response_list_n]
story_title = response_list[0].lstrip("##")
f_p = ":".join(response_list[1:3])
first_part = ":".join(response_list[1:3])
#first_part = {"first_part":{response_list[1].strip() : response_list[2].strip()}}
second_part =":".join(response_list[3:5])
third_part = ":".join(response_list[5:])
print("first_part : ", first_part)
print("second_part : ", second_part)
print("third_part: ", third_part)
story_op = open("output_story.json","a+")
#{story_title: [first_part, second_part, third_part]}
json_story = {"story_title":story_title, "story" :[first_part, second_part, third_part]}
story_op.write(json.dumps(json_story))
story_op.write("\n")
