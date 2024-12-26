from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, CompositeAudioClip, TextClip,VideoFileClip
# from moviepy.editor import * 
import os 
import json
import wave
from pydub import AudioSegment
from fastapi.params import Body
from fastapi import APIRouter
from moviepy.video.VideoClip import * 
from moviepy import Clip
from moviepy.video.fx import *


# from pydantic import BaseModel
#Utube/lib/python3.12/site-packages/moviepy/Clip.py

# class Post_video_gen(BaseModel):
#     auido:str
#     pics: str
#     op_file:str



list_loaded_image = []
video_gen = APIRouter(
    prefix=("/Post_video_gen"),
    tags=["Post_video_gen"]
)


def open_audio(audio_file):
    try:
        wave_file =  wave.open(audio_file, "rb")
        final_audio_length = AudioSegment.from_file(audio_file).duration_seconds
        print(f"audio_length of the the file {audio_file} is {final_audio_length}")
        return AudioSegment.from_file(audio_file), final_audio_length
    except wave.Error:
        get_audio(audio_file, final_audio_length)

def get_dire(data_path):
    content_list =[]
    try:
        for items in os.listdir(data_path):
            item_path = os.path.join(data_path, items)
            content_list.append(item_path)
    except Exception as e:
        return data_path
    return content_list
def get_audio(data_path, final_audio_length):
    list_loaded_audio = AudioSegment.empty()
    print("data_path : Audio ", data_path)
    content_audio=get_dire(data_path)
    print("len(content_audio): ", len(content_audio))
    try:
        for audio_file in content_audio:
            loaded_audio, audio_length= open_audio(audio_file)
            #list_loaded_audio.append(loaded_audio)
            list_loaded_audio+=loaded_audio
            final_audio_length+=audio_length
    except Exception as e:
        loaded_audio, audio_length= open_audio(content_audio)
    list_loaded_audio.export("tmp/combined_audio.wav", format="wav")
    list_loaded = AudioFileClip("tmp/combined_audio.wav")
    return list_loaded, final_audio_length

def open_image(image_file, by_parts, final_audio_length):
    try: 
        _, ext = os.path.splitext(image_file)
        if ext.lower() == '.jpg' or ext.lower() == '.jpeg':
            loaded_image  = ImageClip(image_file).with_duration(by_parts)
            width, height = loaded_image.size
            return loaded_image, width, height
    except Exception as e:
        get_pics(image_file,final_audio_length)

#deprecated
def fadded_video(list_image_obj):
    fade_in_added_list= []
    full_list = []
    for img_n in range(0,2,len(list_image_obj)-1):
        fade_in_added_list.append(FadeIn(list_image_obj[img_n]))
        fade_in_added_list.append(FadeOut(list_image_obj[img_n]))
    print("fade_in_added_list :", fade_in_added_list)
    for img_n in range(len(list_image_obj)-1):
        try:
            full_list.append(fade_in_added_list[img_n])
            full_list.append(list_image_obj[img_n])
            #full_list.append(fade_in_added_list[img_n])
        except IndexError:
            full_list.append(fade_in_added_list[img_n])
            full_list.append(list_image_obj[img_n+1])
    print("full_list :", full_list)
    return full_list

def get_pics(data_path, final_audio_length):
    print("data_path : ", data_path)
    content_image=get_dire(data_path)
    print('len(content_image) : ', len(content_image))
    print("content_image :", content_image)
    by_parts = final_audio_length/len(content_image)
    print("by_parts : ", by_parts)
    for image_file in content_image:
        loaded_image,width, height = open_image(image_file, by_parts, final_audio_length)
        if loaded_image!=None:
            list_loaded_image.append(loaded_image)
    print(list_loaded_image)
    #animation_add = fadded_video(list_loaded_image)
    return concatenate_videoclips(list_loaded_image),width, height

#@video_gen.post("/Post_video_gen/crop_video/{Audio_datapath}/{pics_continuous_video}/{file_name_output_name}/{dimentions_of_img_original_width}/{dimentions_of_img_original_height}")
def make_cropped_video(Audio, pics, file_name,original_width, original_height):
    print("Audio : ", Audio)
    pics.audio = Audio
    pics.write_videofile(f"{file_name}.mp4",fps=24)
    video_file = VideoFileClip(f"{file_name}.mp4")
    new_width = int(original_height * 9 / 16)
    x1 = (original_width - new_width) // 2
    x2 = x1 + new_width
    cropped_clip  = VideoClip.cropped(video_file,x1=x1, y1=0, x2=x2, y2=original_height)
    cropped_clip.write_videofile(f"video/{file_name}.mp4",  codec="libx264")
    os.remove(f"{file_name}.mp4")
    return f"video/{file_name}.mp4"


@video_gen.post("/Post_video_gen/v1")
def Post_video_gen(data :dict = Body(...)):
    Audio, final_audio_length  = get_audio(data["audio"],0)
    print("final_audio_length  : ", final_audio_length) 
    pics,width, height = get_pics(data["pics"], final_audio_length)
    final_croped_video = make_cropped_video(Audio, pics, data["op_file"],width, height)
    # try:
    #     Audio, final_audio_length  = get_audio(data["audio"],0)
    #     print("final_audio_length  : ", final_audio_length) 
    #     pics,width, height = get_pics(data["pics"], final_audio_length)
    #     final_croped_video = make_cropped_video(Audio, pics, data["op_file"],width, height)
    # except Exception as k:
    #     return True
        #return f"{k} Kindly provide a json file as input in the below format {json.load({"audio":"Auido_FIle_path", "pics":"Images_file_path", "op_file": "output_Path_of_the_video"})}"
    return final_croped_video

def get_pics_2(pics, auido_length):
    print("data_path : ", pics)
    content_image=get_dire(pics)
    print('len(content_image) : ', len(content_image))
    print("content_image :", content_image)
    by_parts = auido_length/len(content_image)
    fade_anime =[]
    for i, img in enumerate(content_image):
        _, ext = os.path.splitext(img)
        if ext.lower() == '.jpg' or ext.lower() == '.jpeg':
            loaded_image  = ImageClip(img).with_duration(by_parts)
            width, height = loaded_image.size
        clip = ImageClip(img).with_duration(by_parts)
        clip = CrossFadeIn(clip)
        fade_anime.append(clip)
    return fade_anime, width, height


@video_gen.post("/Post_video_gen/v2")
def Post_video_gen2(data :dict = Body(...)):
    Audio, final_audio_length  = get_audio(data["audio"],0)
    print("final_audio_length  : ", final_audio_length) 
    pics,width, height = get_pics_2(data["pics"], final_audio_length)
    #pics,width, height = get_pics(data["pics"], final_audio_length)
    final_croped_video = make_cropped_video(Audio, pics, data["op_file"],width, height)
    return False


# b = {"audio":"audio/2024-12-17", "pics":"images/2024-12-19", "op_file": "2024-12-20_clips_with_crossfade_cropped"}
# Post_video_gen(b)