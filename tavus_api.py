import requests
import json
open_story_json_file =  open("output_story.json", "r")
obj = [json.loads(i) for i in open_story_json_file]

url = "https://tavusapi.com/v2/speech"

payload = {
    "script": "",
    "replica_id" :"r79e1c033f",
    "callback_url":".Utube_Random_Story_Teller/"
}
headers = {
    "x-api-key": "",
    "Content-Type": "application/json"
}
starting_part = obj[-1]["story"][0]["first_part"]
for name, story in starting_part.items():
    payload["script"]= starting_part[name]
response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)