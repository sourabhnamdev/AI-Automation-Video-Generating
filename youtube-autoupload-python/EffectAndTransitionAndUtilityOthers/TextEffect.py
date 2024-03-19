from moviepy.editor import TextClip, CompositeVideoClip
import numpy as np

class TextEffect:
    def __init__(self, video_clip):
        self.video = video_clip

    def animate_text(self, text, font, font_size, color, start_time, end_time, start_pos, end_pos):
        # Function to interpolate between start_pos and end_pos
        def pos_func(t):
            # Linear interpolation formula: (1 - t) * start + t * end
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * ((t - start_time) / (end_time - start_time))
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * ((t - start_time) / (end_time - start_time))
            return (x, y) if start_time <= t <= end_time else start_pos

        txt_clip = TextClip(text, fontsize=font_size, font=font, color=color).set_duration(end_time - start_time).set_start(start_time).set_position(pos_func)
        # Composite the text clip over the original video clip
        return CompositeVideoClip([self.video, txt_clip.set_start(start_time)])

    # Additional text effects

    def fade_in_text(self, text, font, font_size, color, start_time, end_time):
        txt_clip = (TextClip(text, fontsize=font_size, font=font, color=color)
                    .set_start(start_time)
                    .set_duration(end_time - start_time)
                    .set_position('center')
                    .crossfadein(1))  # 1 second fade-in
        return CompositeVideoClip([self.video, txt_clip])

    def bounce_text(self, text, font, font_size, color, start_time, end_time):
        # Bounce function (sine wave for simplicity)
        def pos_func(t):
            return ('center', 50 * abs(np.sin(2 * np.pi * (t - start_time) / (end_time - start_time))))

        txt_clip = (TextClip(text, fontsize=font_size, font=font, color=color)
                    .set_duration(end_time - start_time)
                    .set_start(start_time)
                    .set_position(pos_func))
        return CompositeVideoClip([self.video, txt_clip])

    def scroll_text(self, text, font, font_size, color, start_time, end_time, direction='up'):
        height = self.video.size[1]
        txt_clip = TextClip(text, fontsize=font_size, font=font, color=color, method='caption', align='South', size=(self.video.size[0], None))
        txt_duration = end_time - start_time

        if direction == 'up':
            y_start = height
            y_end = -txt_clip.size[1]  # Ensuring it scrolls all the way through
        else:  # 'down'
            y_start = -txt_clip.size[1]
            y_end = height

        txt_clip = txt_clip.set_position(lambda t: ('center', y_start + (y_end - y_start) * ((t - start_time) / txt_duration))).set_duration(txt_duration).set_start(start_time)
        
        return CompositeVideoClip([self.video, txt_clip])

# Note: You should create instances of TextEffect with your video clip, then call these methods on the instance.
