from moviepy import AudioClip, CompositeAudioClip, CompositeVideoClip, ImageClip
from moviepy.editor import *
from pydub import AudioSegment

# Load images
image1 = ImageClip("image1.jpg").set_duration(10)
image2 = ImageClip("image2.jpg").set_duration(10)

# Load audio files
audio1 = AudioSegment.from_file("audio1.mp3")
audio2 = AudioSegment.from_file("audio2.mp3")
audio3 = AudioSegment.from_file("audio3.mp3")

# Create audio clips from audio segments
audio_clip1 = AudioClip(audio1)
audio_clip2 = AudioClip(audio2)
audio_clip3 = AudioClip(audio3)

# Combine audio clips
combined_audio = CompositeAudioClip([audio_clip1, audio_clip2, audio_clip3])

# Combine video and audio clips
final_clip = CompositeVideoClip([image1, image2])
final_clip.audio = combined_audio

# Export the final video
final_clip.write_videofile("output_video.mp4", fps=24)