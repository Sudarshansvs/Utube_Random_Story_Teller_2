from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, CompositeAudioClip
import os
import wave
import random
from pydub import AudioSegment
from fastapi.params import Body
from fastapi import APIRouter


#list_loaded_audio = []
list_loaded_image = []
video_gen = APIRouter(
    prefix=("/Post_video_gen"),
    tags=["Post_video_gen"]
)
def export_mp3(data_audio):
    data_audio.export("combined_audio.mp3", format="mp3") 

def open_audio(audio_file):
    try:
        wave_file =  wave.open(audio_file, "rb")
        final_audio_length = AudioSegment.from_file(audio_file).duration_seconds
        print(f"audio_length of the the file {audio_file} is {final_audio_length}")
        return AudioSegment.from_file(audio_file), final_audio_length
    except  wave.Error:
        get_audio(audio_file, final_audio_length)

def get_dire(data_path):
    content_list =[]
    for items in os.listdir(data_path):
        item_path = os.path.join(data_path, items)
        content_list.append(item_path)
    return content_list
def get_audio(data_path, final_audio_length):
    list_loaded_audio = AudioSegment.empty()
    print("data_path : Audio ", data_path)
    content_audio=get_dire(data_path)
    print("len(content_audio): ", len(content_audio))
    for audio_file in content_audio:
        loaded_audio, audio_length= open_audio(audio_file)
        #list_loaded_audio.append(loaded_audio)
        list_loaded_audio+=loaded_audio
        final_audio_length+=audio_length
    list_loaded_audio.export("tmp/combined_audio.wav", format="wav")
    list_loaded = AudioFileClip("tmp/combined_audio.wav")
    return list_loaded, final_audio_length

def open_image(image_file, by_parts, final_audio_length):
    try: 
        _, ext = os.path.splitext(image_file)
        if ext.lower() == '.jpg' or ext.lower() == '.jpeg':
            loaded_image  = ImageClip(image_file).with_duration(by_parts)
            return loaded_image
    except Exception as e:
        get_pics(image_file,final_audio_length)


    

def get_pics(data_path, final_audio_length):
    print("data_path : ", data_path)
    content_image=get_dire(data_path)
    print('len(content_image) : ', len(content_image))
    by_parts = int(final_audio_length/len(content_image))
    print("by_parts : ", by_parts)
    for image_file in content_image:
        loaded_image= open_image(image_file, by_parts, final_audio_length)
        list_loaded_image.append(loaded_image)
    print(list_loaded_image)
    list_image = [i for i in list_loaded_image if i!=None]
    print(list_image)
    return concatenate_videoclips(list_image)


def make_video(Audio, pics):
    print("Audio : ", Audio)
    pics.audio = Audio
    op= "video/op_video.mp4"
    pics.write_videofile(op, fps=24)
    return op


@video_gen.post("/Post_video_gen")
def Post_video_gen(data :dict = Body(...)):
    Audio, final_audio_length  = get_audio(data["audio"],0)
    print("final_audio_length  : ", final_audio_length) 
    pics = get_pics(data["pics"], final_audio_length)
    final_video = make_video(Audio, pics)
    return final_video

# b = {"audio":"audio/2024-12-17", "pics":"images/2024-12-17"}
# Post_video_gen(b)