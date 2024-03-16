import cv2
import numpy as np
import os
import random
from moviepy.editor import ImageClip, concatenate_videoclips
from moviepy.video.fx.all import fadein, fadeout
from moviepy.editor import AudioFileClip
from datetime import datetime
from moviepy.audio.fx.all import audio_loop

video_counter = 0
def generate_video():
    global video_counter  # Declare video_counter as a global variable
    print("Generating video...")
    video_counter += 1
    # Current date and time ko format karke ek string me convert karein
    
    # Define the size to which all images will be resized
    width, height = 1200, 2000

    # Path to your folder containing images
    image_folder = 'G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\DataLibrary\\Images\\Hero Heroin'
    # audio_path = 'G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\DataLibrary\\audio\\your_song.mp3'
    # Path to your folder containing audio files
    audio_folder = 'G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\DataLibrary\\audio'
    # Get all image files from the folder
    all_images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Randomly select up to 5 images, depending on how many are available
    num_images_to_select = min(len(all_images), 10)
    selected_images = random.sample(all_images, num_images_to_select)

    # Generate full path for each selected image
    image_paths = [os.path.join(image_folder, img) for img in selected_images]

    # Total duration of the video
    total_video_duration = 60  # seconds

    # Calculate display duration for each image to fit into total video duration
    num_images = len(image_paths)
    image_display_duration = total_video_duration / num_images

    # Duration of fade in and fade out
    fade_duration = 1

    # Create a sequence of images as video clips
    clips = []
    for img_path in image_paths:
        img_clip = ImageClip(img_path).set_duration(image_display_duration)
        img_clip = img_clip.resize(newsize=(width, height))
        img_clip = fadein(img_clip, fade_duration).fadeout(fade_duration) 
        clips.append(img_clip)

    # Concatenate all the clips together
    final_clip = concatenate_videoclips(clips, method="compose")

    # Randomly select an audio file from the folder
    all_audio_files = [f for f in os.listdir(audio_folder) if f.endswith(('.mp3', '.wav'))]
    selected_audio_file = random.choice(all_audio_files)
    audio_path = os.path.join(audio_folder, selected_audio_file)

    audio_clip = AudioFileClip(audio_path)

    

    # If audio duration is shorter than video duration, loop the audio clip
    if audio_clip.duration < total_video_duration:
       audio_clip = audio_loop(audio_clip, duration=total_video_duration)

    # If audio duration is shorter than video duration, loop the audio clip
    if audio_clip.duration > total_video_duration:
       # Load and set the audio of the final video clip
       audio_clip = audio_clip.subclip(0, total_video_duration)
       

    final_clip = final_clip.set_audio(audio_clip)
    # Output file will be in .mp4 format
    final_output_path = f'G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\Generated Videos\\10_images_video_{video_counter}.mp4'

    # Write the result to a new file
    final_clip.write_videofile(final_output_path, codec="libx264", audio_codec="aac", fps=24)

    # calling youtube video uploading method
    # if video_counter > 5:
    #    print("calling uploading video method")
    #    upload_on_youtube_auto()
       

