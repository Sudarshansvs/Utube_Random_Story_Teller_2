from moviepy import ImageClip, concatenate_videoclips,ImageSequenceClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, TextClip,VideoFileClip
# from moviepy.editor import * 
import os 
import cv2
import json
import wave
from pydub import AudioSegment
from fastapi.params import Body
from fastapi import APIRouter
from moviepy.video.VideoClip import * 
from moviepy import Clip
from moviepy.video.fx import FadeIn , FadeOut, CrossFadeIn, CrossFadeOut,Resize
from moviepy.video.compositing.CompositeVideoClip import * 
import numpy as np 
import regex as re

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

#depricated
# def open_image(image_file, by_parts, final_audio_length):
#     try: 
#         _, ext = os.path.splitext(image_file)
#         if ext.lower() == '.jpg' or ext.lower() == '.jpeg':
#             blur_loaded_iumg = Image.open(image_file)
#             b1 = blur_loaded_iumg.save("test","JPG")
#             b2 = Image.open("test").ImageFilter.BLUR
#             blur_loaded_iumg.save("test")
#             #blur_loaded_iumg_1 = blur_loaded_iumg.filter(filter=HeadBlur)
#             loaded_image  = ImageClip(image_file).with_duration(by_parts)
#             blur_loaded_iumg_1 = ImageClip(f"test.jpeg").with_duration(by_parts)
#             width, height = loaded_image.size
#             return blur_loaded_iumg_1, loaded_image, width, height
#     except Exception as e:
#         get_pics(image_file,final_audio_length)

#deprecated waste of time

# TypeError: CrossFadeIn.__init__() takes 2 positional arguments but 3 were given

def fade_in_and_out(image_dir,by_parts):
    images = sorted([os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(('jpg', 'jpeg', 'png', 'gif'))])
    clips = []
    for i, image_path in enumerate(images):
        # Create a clip from the image
        clip = ImageSequenceClip([image_path], durations=[by_parts])
        # Apply fade-in for the first image, fade-out for the last image, and both for others
        if i == 0:  # Apply fade-in for the first image
            clip = CrossFadeIn(clip, 2)
        elif i == len(images) - 1:  # Apply fade-out for the last image
            clip = CrossFadeOut(clip, 2)
        else:  # Apply both fade-in and fade-out for intermediate images
            clip = CrossFadeIn(clip, 2)
    clips.append(clip)
    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile("output_video_with_fades.mp4", fps=24)
    print("output_video_with_fades.mp4")


def add_fading_animation(content_image,num_frames=30):
    frames = []
    loaded_image = []
    for file in range(len(content_image)-1):
        img1 = Image.open(content_image[file]).convert("RGBA")
        img2 = Image.open(content_image[file+1]).convert("RGBA")
        for frame in range(num_frames):
            alpha = frame / (num_frames - 1)
            blended_image = Image.blend(img1, img2, alpha)
            frame1 = np.array(blended_image)
            if frame1.shape[2] == 4:
                frame1 = cv2.cvtColor(frame1, cv2.COLOR_RGBA2BGR)
            frames.append(frame)
        blended_image.save(f"tmp/img_{file}_{frame:03d}.png")
        loaded_image.append(ImageClip(f"tmp/img_{file}_{frame:03d}.png"))
    print("loaded_image : ", loaded_image)
    return loaded_image

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
# def fadded_video(list_image_obj):
#     fade_in_added_list= []
#     full_list = []
#     for img_n in range(len(list_image_obj)-1):
#         fade_in_added_list.append(CrossFadeIn(list_image_obj[img_n]))
#         fade_in_added_list.append(CrossFadeOut(list_image_obj[img_n]))
#     print("fade_in_added_list :", fade_in_added_list)
#     for img_n in range(len(list_image_obj)-1):
#         try:
#             full_list.append(fade_in_added_list[img_n])
#             full_list.append(list_image_obj[img_n])
#             #full_list.append(fade_in_added_list[img_n])
#         except IndexError:
#             full_list.append(fade_in_added_list[img_n])
#             full_list.append(list_image_obj[img_n+1])
#     print("full_list :", full_list)
#     return clips_array(full_list)


def fadded_video(list_image_obj):
    fade_in_added_list= []
    full_list = []
    for img_n in range(len(list_image_obj)-1):
        fade_in_added_list.append(CrossFadeIn(list_image_obj[img_n]))
        fade_in_added_list.append(list_image_obj[img_n])
        fade_in_added_list.append(CrossFadeOut(list_image_obj[img_n]))
    print("fade_in_added_list :", fade_in_added_list)

    print("full_list :", full_list)
    return full_list
def open_mov(file):
    video = VideoFileClip(file)
    video_clip = video.subclipped(0.5, 0.6)
    output_video_path = "output_video_clip.mp4"
    video_clip.write_videofile(output_video_path, codec="libx264", fps=24)
    video = VideoFileClip(output_video_path)
    return video
def get_pics(data_path, final_audio_length):
    #print("data_path : ", data_path)
    content_image=get_dire(data_path)
    # print('len(content_image) : ', len(content_image))
    # print("content_image :", content_image)
    by_parts = final_audio_length/len(content_image)
    #print("by_parts : ", by_parts)
    #fade_in_and_out(data_path,by_parts)
    #x = add_fading_animation(content_image)
    #not_none_list = [i for i in x if i==None]
    for image_file in content_image:
        loaded_image,width, height = open_image(image_file, by_parts, final_audio_length)
        if loaded_image!=None:
            list_loaded_image.append(loaded_image)
    #print(list_loaded_image)
    #list_loaded_image.extend(not_none_list)
    # print("list_loaded_image_extended :", list_loaded_image)
    # animation_add = fadded_video(list_loaded_image)
    clip_for_transition = open_mov("stockfootage0696.mov")
    return concatenate_videoclips(list_loaded_image,transition=clip_for_transition),width, height

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

def adding_zoom_in_action(videoclip, output_file):
    video = VideoFileClip(videoclip)
    video_duration = (video.duration)/2
    def zoom_in(t):
        zoom_factor = 1 + 0.5 * (t / video_duration)**10  # Gradually zoom from 1 to 1.5
        return zoom_factor
    def zoom_out(t):
        zoom_factor = 1.5 - 0.5 * (t / video_duration)**10  # Gradually zoom from 1 to 1.5
        return zoom_factor if zoom_factor>0 else (0 + 0.15 * (t / video_duration))
    zoom_in_video = video.resized(zoom_in,Resize.resizer)
    zoom_out_video = video.resized(zoom_out,Resize.resizer)
    gradual_zoomed_video = concatenate_videoclips([zoom_in_video,zoom_out_video])
    gradual_zoomed_video.write_videofile(f"video/{output_file}_zoom_tryout.mp4", codec="libx264", fps=24)
    return f"video/{output_file}_zoom_tryout.mp4"

def clear_cache(op,zoom):
    os.remove("output_video_clip.mp4")
    os.remove("tmp/combined_audio.wav")
    db = open("Data_base.csv","a+")
    db.write("\n")
    db.writelines(f"video_generated,{op},{f"video/{op}: zoomed video if any {zoom}"}")


@video_gen.post("/Post_video_gen")
def Post_video_gen(data :dict = Body(...)):
    Audio, final_audio_length  = get_audio(data["audio"],0)
    print("final_audio_length  : ", final_audio_length) 
    pics,width, height = get_pics(data["pics"], final_audio_length)
    final_croped_video = make_cropped_video(Audio, pics, data["op_file"],width, height)
    zoom = adding_zoom_in_action(final_croped_video, data["op_file"]) if data["zoom"]=="True" else None
    clear_cache(data["op_file"],zoom)
    return final_croped_video, zoom



# b = {"audio":"audio/2024-12-28", "pics":"images/2024-12-28", "op_file": "A_12_28_I_12_28", "zoom":"False"}
# Post_video_gen(b)
