from dotenv import load_dotenv
import os
import datetime
import json
from PIL import Image
from fastapi import APIRouter
from auth import image_gen

image_generater = APIRouter(
    prefix=('/image_generater'),
    tags = ['image_generater']
)
load_dotenv()

def pas_story(count):
    Story_to_read = open("output_story.json", "r")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    story_listobj = [json.loads(i) for i in Story_to_read]
    tittle_story = story_listobj[-1]
    story = tittle_story["story"]
    filtered_tsory = []
    img_name = f"{str.replace(tittle_story["story_title"], " ", "_")}_{count}.jpg"
    for part in story:
        if ":" in part:
            filtered_tsory.append(part.split(":"))
    image_story = "".join(filtered_tsory[count][1:])
    print("filtered_tsory : ", filtered_tsory)
    print("filtered_tsory[{}][1:] : ".format(count), image_story)
    return image_story, img_name

# output is a PIL.Image object
@image_generater.get('/image_generater')
def Image_generator():
    client = image_gen()
    count=0
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs("images/{}".format(timestamp), exist_ok=True)
    while count!=3:
        image_to_genarate, img_name = pas_story(count)
        image = client.text_to_image(image_to_genarate)
        image.save("images/{}/{}".format(timestamp,img_name), "JPEG")
        count+=1
    return "Image genaration completed. Kindly check the directory images/{}".format(timestamp)


    

