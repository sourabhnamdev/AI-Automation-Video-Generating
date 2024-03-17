from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, clips_array
from moviepy.video.fx import fadein, fadeout
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.VideoClip import ImageClip
import cv2
import numpy as np

class VideoTransitions:
    def __init__(self, video_path):
        self.video = VideoFileClip(video_path)

    def add_fadein_and_fadeout(self, video2, duration=1):
        # Correcting method name and logic according to MoviePy conventions.
        first_clip = self.video.fx(fadeout, duration)
        second_clip = video2.fx(fadein, duration)
        return concatenate_videoclips([first_clip, second_clip], padding=-duration, method="compose")
    
    def wipe_transition(self, video2, duration=1):
        # Wipe transition: Let's assume a simple left-to-right wipe for this example.
        # MoviePy doesn't directly support wipes, so we simulate it using cropping and composition.
        wipe_effect = lambda t: ('crop', 0, 0, int(t/duration * video2.size[0]), video2.size[1])
        second_clip_wipe = video2.fl_image(lambda img, t: wipe_effect(t)[1](img) if t < duration else img)
        return CompositeVideoClip([self.video, second_clip_wipe.set_start(self.video.duration - duration)])
        
    def slide_transition(self, video2, direction='left', duration=1):
        # Slide transition: We move one video out and another in from a direction.
        if direction == 'left':
            slide_fx = lambda clip, t: ('translate', (-t/duration * clip.size[0], 0))
        elif direction == 'right':
            slide_fx = lambda clip, t: ('translate', (t/duration * clip.size[0], 0))
        # For simplicity, handling left and right only. Extend as needed.
        
        first_clip_slide = self.video.fl_image(lambda img, t: slide_fx(self.video, t)[1](img) if t < duration else img)
        second_clip_slide = video2.set_start(duration).fl_image(lambda img, t: slide_fx(video2, t)[1](img) if t < duration else img)
        return CompositeVideoClip([first_clip_slide, second_clip_slide], size=self.video.size)

    def dissolve_transition(self, video2, duration=1):
        # Correcting dissolve implementation.
        first_clip = self.video.crossfadeout(duration)
        second_clip = video2.crossfadein(duration)
        return concatenate_videoclips([first_clip, second_clip], padding=-duration, method="compose")
    
    # Zoom Transition:
    def zoom_transition(self, video2, duration=1, zoom_factor=4):
        # Zoom in on the end of the first clip
        final_frame = self.video.to_ImageClip(self.video.duration)
        zoom_in = final_frame.resize(lambda t: 1 + zoom_factor * (1 - t / duration))  # Zoom in
        zoom_in = zoom_in.set_duration(duration)

        # Zoom out from the start of the second clip
        start_frame = video2.to_ImageClip(0)
        zoom_out = start_frame.resize(lambda t: 1 + zoom_factor * (t / duration))  # Zoom out
        zoom_out = zoom_out.set_duration(duration)

        # Combine the two clips
        final_clip = concatenate_videoclips([self.video, zoom_in, zoom_out, video2], method="compose")
        return final_clip

    # Spin Transition:
    def spin_transition(self, video2, duration=1, spin_cycles=2):
        # Spin out the first clip
        spin_out = self.video.fl_time(lambda t: rotate(self.video, t/duration * 360 * spin_cycles))
        spin_out = spin_out.set_end(duration)

        # Spin in the second clip
        spin_in = video2.fl_time(lambda t: rotate(video2, (1 - t/duration) * 360 * spin_cycles))
        spin_in = spin_in.set_start(self.video.duration).set_duration(duration)

        # Combine the two clips
        final_clip = concatenate_videoclips([self.video, spin_out, spin_in, video2], method="compose")
        return final_clip

    # Heartbeat Transition:
    def heartbeat_transition(self, video2, duration=1, beat_times=2):
    # Define the heartbeat effect
        def heartbeat_effect(clip, times, duration):
            beats = []
            for i in range(times):
                beat_duration = duration / (2 * times)
                beat = clip.fx(resize, lambda t: 1 + 0.1 * (1 if (t // beat_duration) % 2 == 0 else -1), apply_to=['mask', 'video'])
                beat = beat.set_duration(beat_duration)
                beats.append(beat)
            return concatenate_videoclips(beats)
    
        # Apply heartbeat to the end of the first clip and start of the second
        heartbeat_end = heartbeat_effect(self.video.subclip(max(0, self.video.duration - duration), self.video.duration), beat_times, duration)
        heartbeat_start = heartbeat_effect(video2.subclip(0, min(duration, video2.duration)), beat_times, duration)

        # Combine the two clips
        final_clip = concatenate_videoclips([self.video, heartbeat_end, heartbeat_start, video2], method="compose")
        return final_clip

    


