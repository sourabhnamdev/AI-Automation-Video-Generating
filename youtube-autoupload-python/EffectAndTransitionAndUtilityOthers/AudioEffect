from moviepy.editor import AudioFileClip
import numpy as np
from scipy.signal import butter, lfilter

class AudioEffect:
    def __init__(self, audio_path):
        self.audio = AudioFileClip(audio_path)

    def apply_echo(self, delay, decay):
        """Apply an echo effect to the audio."""
        # This is a simplified placeholder. Actual implementation would require
        # more sophisticated audio manipulation libraries like PyDub.
        def make_frame(t):
            original = self.audio.get_frame(t)
            echo_time = int(delay * self.audio.fps)
            if t > delay:
                echo = decay * self.audio.get_frame(t - delay)
                return (original + echo).astype(np.float32)
            return original
        return self.audio.fl(make_frame)

    def apply_reverb(self, room_size):
        """Simulate reverb effect indicative of room size."""
        # Placeholder for reverb; actual implementation requires convolution with room impulse response
        pass

    def apply_bandpass_filter(self, low, high):
        """Apply a bandpass filter to allow frequencies within a certain range."""
        def butter_bandpass(lowcut, highcut, fs, order=5):
            nyq = 0.5 * fs
            low = lowcut / nyq
            high = highcut / nyq
            b, a = butter(order, [low, high], btype='band')
            return b, a

        def bandpass_filter(data, lowcut, highcut, fs, order=5):
            b, a = butter_bandpass(lowcut, highcut, fs, order=order)
            y = lfilter(b, a, data)
            return y

        def make_frame(t):
            frame_rate = self.audio.fps
            return bandpass_filter(self.audio.get_frame(t), low, high, frame_rate)

        return self.audio.fl(make_frame)

    # New Effect: Fade In
    def apply_fade_in(self, duration):
        """Apply a fade-in effect over the specified duration."""
        return self.audio.fx(vfx.audio_fadein, duration)

    # New Effect: Fade Out
    def apply_fade_out(self, duration):
        """Apply a fade-out effect over the specified duration."""
        return self.audio.fx(vfx.audio_fadeout, duration)

    # New Effect: Increase Volume
    def increase_volume(self, factor):
        """Increase volume by a specified factor."""
        return self.audio.volumex(factor)

    # New Effect: Lower Volume
    def lower_volume(self, factor):
        """Lower volume by a specified factor."""
        return self.audio.volumex(1.0 / factor)
