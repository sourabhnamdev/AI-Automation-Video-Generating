import cv2
import numpy as np
import os
import random
from moviepy.editor import ImageClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout
from moviepy.editor import AudioFileClip

# Define the size to which all images will be resized
width, height = 1200, 2000

# Path to your folder containing images
image_folder = 'C:\\Automate\\AI-Automation-Video-Generating\\youtube-autoupload-python\\DataLibrary\\Images\\Hero Heroin'
audio_path = 'C:\\Automate\\AI-Automation-Video-Generating\\youtube-autoupload-python\\DataLibrary\\audio\\Instrumental\\your_song.mp3'

# Get all image files from the folder
all_images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Randomly select up to 5 images, depending on how many are available
num_images_to_select = min(len(all_images), 5)  # Choose 5 or the total number of images if less than 5
selected_images = random.sample(all_images, num_images_to_select)

# Generate full path for each selected image
image_paths = [os.path.join(image_folder, img) for img in selected_images]

# Total duration of the video
total_video_duration = 60  # seconds

# Determine the number of images
num_images = len(image_paths)

# Calculate display duration for each image to fit into total video duration
image_display_duration = total_video_duration / num_images

# Duration of fade in and fade out
fade_duration = 1  # Adjust based on your preference, but ensure total duration is not exceeded

# Create a sequence of images as video clips
clips = []
for img_path in image_paths:
    # Create an ImageClip and set its duration
    img_clip = ImageClip(img_path).set_duration(image_display_duration)
    
    # Resize the clip
    img_clip = img_clip.resize(newsize=(width, height))
    
    # Add fade in and fade out effects
    img_clip = fadein(img_clip, fade_duration).fadeout(fade_duration)
    
    # Add the clip to the list of clips
    clips.append(img_clip)

# Concatenate all the clips together
final_clip = concatenate_videoclips(clips, method="compose")

# Load and set the audio of the final video clip
audio_clip = AudioFileClip(audio_path).subclip(0, total_video_duration)  # Use only the first 60 seconds of the audio
final_clip = final_clip.set_audio(audio_clip)

# Output file will be in .mp4 format
final_output_path = 'C:\\Automate\\AI-Automation-Video-Generating\\youtube-autoupload-python\\Generated Videos\\Love\\5_images_video.mp4'

# Write the result to a new file
final_clip.write_videofile(final_output_path, codec="libx264", audio_codec="aac", fps=24)
