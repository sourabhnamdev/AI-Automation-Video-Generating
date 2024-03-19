from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video import fx as vfx
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.VideoClip import ImageClip
import cv2
import numpy as np

class VideoEffects:
    def __init__(self, video_path):
        self.video = VideoFileClip(video_path)
    
    def apply_effect(self, effect):
        effects = {
            'blur': lambda clip: clip.fx(vfx.blur, radius=2),
            'mirror': lambda clip: clip.fx(vfx.mirror_x),
            'black_and_white': lambda clip: clip.fx(vfx.blackwhite),
            'invert_colors': lambda clip: clip.fx(vfx.invert_colors),
            'painting': lambda clip: clip.fx(vfx.painting),
            'colorx': lambda clip: clip.fx(vfx.colorx, factor=2),
            'speed': lambda clip: clip.fx(vfx.speedx, factor=2),
            'contrast': lambda clip: clip.fx(vfx.lum_contrast, contrast=1.5, lum=50)
        }
        if effect not in effects:
            raise ValueError(f"Effect '{effect}' is not supported")
        return effects[effect](self.video)

    def adjust_colors(self, brightness=1.0, contrast=1.0, saturation=1.0):
        if not (0 <= brightness <= 2 and 0 <= contrast <= 2 and 0 <= saturation <= 2):
            raise ValueError("Color settings must be within the range [0, 2]")
        # Note: This is a simplified example. Actual implementation might differ
        # since MoviePy doesn't directly support all these adjustments.
        # Below is a placeholder for brightness adjustment. You'll need to adapt it for other properties.
        return self.video.fx(vfx.colorx, factor=brightness)

    def change_speed(self, factor):
        if factor <= 0:
            raise ValueError("Speed factor must be greater than zero")
        return self.video.fx(vfx.speedx, factor)
    
#Special Effects

    def apply_mosaic(self, block_size=10):
         # Mosaic effect: Apply a pixelation effect to the video.
         # Placeholder for actual implementation using CV2 or similar for effect application.
         pass

    def apply_glow(self, intensity=1):
         # Glow effect: Apply a glow effect to the video.
         # This effect is not directly available in MoviePy, so you'd need to implement it using a custom method or an external library.
         pass
    
    # =============================
    # 1. Sketch Effect (Pencil Sketch with OpenCV):
 

    def apply_sketch_effect(self):
        def make_frame(t):
            frame = self.video.get_frame(t)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            inverted_frame = 255 - gray_frame
            blurred_frame = cv2.GaussianBlur(inverted_frame, (21, 21), 0)
            inverted_blurred = 255 - blurred_frame
            sketch_frame = cv2.divide(gray_frame, inverted_blurred, scale=256.0)
            return cv2.cvtColor(sketch_frame, cv2.COLOR_GRAY2BGR)  # Convert back to BGR for MoviePy
        
        return self.video.fl(make_frame)  # Apply the effect to each frame
    
    # 2. Neon Outline Effect:
    def neon_outline_effect(self, color=(0, 255, 0)):
        def make_frame(t):
            frame = self.video.get_frame(t)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            edges_colored = np.zeros_like(frame)
            edges_colored[edges != 0] = color
            return cv2.addWeighted(frame, 0.8, edges_colored, 0.2, 0)
        return self.video.fl(make_frame)    
    # 3. Auto HDR Effect:
    def auto_hdr_effect(self):
        def make_frame(t):
            frame = self.video.get_frame(t)
            # Convert to LAB color space
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
            # Split channels
            l, a, b = cv2.split(lab)
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L-channel
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            # Convert back to BGR
            return cv2.cvtColor(limg, cv2.COLOR_Lab2BGR)
        return self.video.fl(make_frame)
    
    # 4. Grainy Slide:
    def apply_grainy_slide_effect(self, grain_level=5):
        def make_frame(t):
            frame = self.video.get_frame(t)
            grain = (np.random.rand(*frame.shape) * 255 * grain_level).astype(np.uint8)
            return cv2.add(frame, grain)  # Add the grain overlay to the frame
        
        return self.video.fl(make_frame)  # Apply the grainy effect to each frame
    
    # 5. Scene Replica:
    # This would involve recreating a scene from one video in another context or style. This is highly context-specific and would typically involve deep learning or advanced editing techniques beyond the scope of basic library functions.

    # 6. Light Flare:
    # Adding a light flare or lens flare effect would usually involve overlaying a pre-rendered flare image or animation onto your video, potentially animated or positioned based on the scene's lighting.

    # 7. Focus Overlay (Bokeh or Depth of Field):
    # Simulating a depth of field effect, where parts of the image are blurred while others remain in focus, can be complex and would typically use a mask or alpha channel to define focus areas.

    # 8. Vignette:
    def apply_vignette(self, strength=0.5):
        def make_frame(t):
            frame = self.video.get_frame(t)
            height, width = frame.shape[:2]
            x = np.arange(width)
            y = np.arange(height)
            X, Y = np.meshgrid(x, y)
            radius = np.sqrt((X - width / 2) ** 2 + (Y - height / 2) ** 2)
            vignette = np.clip((1 - radius / max(width, height) * 2) ** strength, 0, 1)
            vignette = np.tile(vignette[:, :, None], [1, 1, 3])
            return (frame * vignette).astype(np.uint8)
        
        return self.video.fl(make_frame)
    
    def vignette_effect(self, strength=0.5):
        center_x = self.video.size[0] / 2
        center_y = self.video.size[1] / 2
        max_radius = np.sqrt(center_x**2 + center_y**2)
        vignette = np.zeros((self.video.size[1], self.video.size[0]), np.uint8)

        for y in range(self.video.size[1]):
            for x in range(self.video.size[0]):
                radius = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                vignette[y, x] = 255 * np.clip(1 - strength * radius / max_radius, 0, 1)

        def make_frame(t):
            frame = self.video.get_frame(t)
            frame_vignetted = cv2.merge([cv2.bitwise_and(frame[:,:,i], frame[:,:,i], mask=vignette) for i in range(3)])
            return frame_vignetted
        return self.video.fl(make_frame)
    
    # 9. Cartoon Tone:
    def cartoon_effect(self):
        def make_frame(t):
            frame = self.video.get_frame(t)
            # Edge detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            # Color quantization
            # Convert to LAB color space for better clustering
            data = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
            data = data.reshape((-1, 3))
            data = np.float32(data)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
            _, labels, centers = cv2.kmeans(data, 9, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            centers = np.uint8(centers)
            result_data = centers[labels.flatten()]
            result_image = result_data.reshape((frame.shape))
            result_image = cv2.cvtColor(result_image, cv2.COLOR_Lab2BGR)
            # Combine edges and quantized colors
            cartoon = cv2.bitwise_and(result_image, result_image, mask=edges)
            return cartoon
        return self.video.fl(make_frame)

    # 10. Bevel Effect:
    # Creating a bevel effect on video frames involves manipulating light and shadow to create the illusion of depth. This is complex and not directly supported by MoviePy or OpenCV in a video context.

    # 11. Gaussian Blur:
    def gaussian_blur_effect(self, kernel_size=5):
        def make_frame(t):
            frame = self.video.get_frame(t)
            blurred_frame = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
            return blurred_frame
        return self.video.fl(make_frame)

    # 12. Mosaic:
    def mosaic_effect(self, block_size=10):
        def make_frame(t):
            frame = self.video.get_frame(t)
            # Resize down and up to create the mosaic effect
            small_frame = cv2.resize(frame, (frame.shape[1]//block_size, frame.shape[0]//block_size))
            mosaic_frame = cv2.resize(small_frame, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)
            return mosaic_frame
        return self.video.fl(make_frame)

    # 13. Light Flare:
    def light_flare_effect(self, flare_path, position=(100, 100)):
        flare = ImageClip(flare_path).set_duration(self.video.duration).set_pos(position)
        return CompositeVideoClip([self.video, flare])

    # 14. Focus Overlay:
    def focus_overlay_effect(self, focus_center, focus_radius, blur_strength=5):
        def make_frame(t):
            frame = self.video.get_frame(t)
            # Create a mask for the focus area
            mask = np.zeros_like(frame)
            cv2.circle(mask, focus_center, focus_radius, (255, 255, 255), -1, cv2.LINE_AA)
            blurred_frame = cv2.GaussianBlur(frame, (blur_strength, blur_strength), 0)
            # Combine the blurred frame and the original frame using the mask
            focused_frame = np.where(mask==np.array([255, 255, 255]), frame, blurred_frame)
            return focused_frame
        return self.video.fl(make_frame)

