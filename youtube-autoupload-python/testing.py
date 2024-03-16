from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx import all as vfx

# Load the background video clip
background_clip = VideoFileClip("G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\Generated Videos\\Love\\10_images_video_2.mp4")

# Add a text overlay at 10 seconds with specified text
txt_clip = TextClip("Hello, World!", fontsize=50, color='white')
txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(5)  # Position and duration

# Composite the text overlay on the background video clip
video_with_text = CompositeVideoClip([background_clip, txt_clip])

# Apply a filter - Increase brightness by 30%
filtered_clip = video_with_text.fx(vfx.colorx, 1.3)

# Save the final video
filtered_clip.write_videofile("G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\Generated Videos\\Love\\final_video.mp4")
