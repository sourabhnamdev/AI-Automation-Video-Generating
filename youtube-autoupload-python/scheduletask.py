import schedule
import time
from scheduleautogeneratevideo import generate_video

video_counter = 0  # Counter for 'generate_video'
upload_counter = 0  # Counter for 'upload_on_youtube_auto'

video_completed = False  # Flag to indicate if video generation is completed

def job_for_video():
    global video_counter, video_completed
    
    print("Scheduled task for video generation started.")
    generate_video()
    video_counter += 1  # Increment the counter each time the job runs

    if video_counter >= 5:
        print("Video generation completed.")
        video_completed = True  # Set the flag to True
        
# Schedule 'generate_video' function to run every 3 minutes
schedule.every(20).seconds.do(job_for_video)

while True:
    schedule.run_pending()
    time.sleep(1)
