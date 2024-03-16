import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout
from moviepy.editor import ImageClip, AudioFileClip

# Define the size to which all images will be resized
width, height = 1200, 2000

# Path to your images and audio
image_paths = [
    'G:\\Automation_Video_Project\\videoapp\\Data\\Images\\Hero Heroin\\boy.jpg',
    'G:\\Automation_Video_Project\\videoapp\\Data\\Images\\Hero Heroin\\sa.jpg',
    'G:\\Automation_Video_Project\\videoapp\\Data\\Images\\Hero Heroin\\wa.jpg'
]
audio_path = 'G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\DataLibrary\\audio\\your_song.mp3'

# Load the audio to determine its duration
audio_clip = AudioFileClip(audio_path)
audio_duration = audio_clip.duration  # Duration of the audio in seconds

# Determine the number of images based on the audio duration
num_images = len(image_paths)
image_display_duration = audio_duration / num_images  # Each image duration based on audio length

# Duration of fade in and fade out
fade_duration = 1  # Adjust based on your preference

# Create a sequence of images as video clips
clips = []
for img_path in image_paths:
    # Create an ImageClip and set its duration
    img_clip = ImageClip(img_path).set_duration(image_display_duration)
    
    # Resize the clip (Note: 'resize' is a method of ImageClip)
    img_clip = img_clip.resize(newsize=(width, height))
    
    # Add fade in and fade out effects
    img_clip = fadein(img_clip, fade_duration).fadeout(fade_duration)
    
    # Add the clip to the list of clips
    clips.append(img_clip)

# Concatenate all the clips together
final_clip = concatenate_videoclips(clips, method="compose")

# Set the audio of the final video clip as your audio file
final_clip = final_clip.set_audio(audio_clip)

# Output file will be in .mp4 format
final_output_path = 'G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\videos\\DependOnAudioDuration_video.mp4'

# Write the result to a new file
final_clip.write_videofile(final_output_path, codec="libx264", audio_codec="aac",fps=24)
