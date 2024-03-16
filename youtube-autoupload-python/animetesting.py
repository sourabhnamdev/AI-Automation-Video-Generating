# # import cv2
# # import numpy as np

# # def apply_cartoon_effect_to_frame(frame):
# #     # Convert to gray scale
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
# #     # Apply median blur to reduce image noise
# #     gray_blurred = cv2.medianBlur(gray, 7)
    
# #     # Detect edges in the image using adaptive thresholding
# #     edges = cv2.adaptiveThreshold(gray_blurred, 255,
# #                                   cv2.ADAPTIVE_THRESH_MEAN_C,
# #                                   cv2.THRESH_BINARY, blockSize=9, C=2)
    
# #     # Apply bilateral filter to smoothen the colors
# #     filtered = frame
# #     for _ in range(2):  # Applying the filter multiple times
# #         filtered = cv2.bilateralFilter(filtered, d=9, sigmaColor=75, sigmaSpace=75)
    
# #     # Reduce the color palette of the image
# #     data = np.float32(filtered).reshape((-1, 3))
# #     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
# #     _, label, center = cv2.kmeans(data, 8, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
# #     center = np.uint8(center)
# #     result = center[label.flatten()]
# #     result = result.reshape(frame.shape)
    
# #     # Combine edges and color-quantized image
# #     cartoon = cv2.bitwise_and(result, result, mask=edges)
    
# #     return cartoon

# # def convert_video_to_cartoon(input_video_path, output_video_path):
# #     # Read the video
# #     cap = cv2.VideoCapture(input_video_path)
# #     if not cap.isOpened():
# #         print(f"Error: Unable to open video at {input_video_path}")
# #         return
    
# #     # Get video properties
# #     fps = cap.get(cv2.CAP_PROP_FPS)
# #     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# #     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# #     codec = cv2.VideoWriter_fourcc(*'MP4V')  # Adjust based on your video; 'XVID' for .avi
    
# #     # Prepare output video writer
# #     out = cv2.VideoWriter(output_video_path, codec, fps, (width, height))
    
# #     while True:
# #         ret, frame = cap.read()
# #         print ('ret')
# #         if not ret:
# #             break
        
# #         # Apply cartoon effect
# #         cartoon_frame = apply_cartoon_effect_to_frame(frame)
        
# #         # Write the frame
# #         out.write(cartoon_frame)
    
# #     # Release resources
# #     cap.release()
# #     out.release()
# #     print("Conversion complete!")

# # # Usage
# # convert_video_to_cartoon('C:\\Users\\dell\\Downloads\\lovevideo.mp4', 'C:\\Users\\dell\\Downloads\\cartoon_video.mp4')
# # ==============================================================
# import cv2
# import numpy as np

# def cartoonize_image(img):
#     # Step 1: Apply a bilateral filter to reduce the color palette of the image.
#     img_color = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

#     # Step 2: Convert to grayscale and apply median blurring
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.medianBlur(gray, 7)

#     # Step 3: Create an edge mask using adaptive thresholding
#     edges = cv2.adaptiveThreshold(gray, 255,
#                                   cv2.ADAPTIVE_THRESH_MEAN_C,
#                                   cv2.THRESH_BINARY, blockSize=9, C=2)

#     # Step 4: Combine the color image with the edge mask
#     edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
#     img_cartoon = cv2.bitwise_and(img_color, edges)

#     return img_cartoon

# def process_video(input_video_path, output_video_path):
#     # Capture video
#     cap = cv2.VideoCapture(input_video_path)
#     # Video writer
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break  # End of video
#         # Apply cartoon effect
#         cartoon_frame = cartoonize_image(frame)
#         # Write the frame into the file 'output_video.mp4'
#         out.write(cartoon_frame)

#     cap.release()
#     out.release()

# # Usage
# process_video('C:\\Users\\dell\\Downloads\\dance.mp4', 'C:\\Users\\dell\\Downloads\\your_output_video.mp4')

# ======================================================= 
# image to cartoon code
# import argparse
# import time
# import numpy as np
# from collections import defaultdict
# from scipy import stats
# import cv2


# def cartoonize(image):
#     """
#     convert image into cartoon-like image
#     image: input PIL image
#     """

#     output = np.array(image)
#     x, y, c = output.shape
#     # hists = []
#     for i in range(c):
#         output[:, :, i] = cv2.bilateralFilter(output[:, :, i], 5, 50, 50)
#         # hist, _ = np.histogram(output[:, :, i], bins=np.arange(256+1))
#         # hists.append(hist)
#     edge = cv2.Canny(output, 100, 200)

#     output = cv2.cvtColor(output, cv2.COLOR_RGB2HSV)

#     hists = []
#     #H
#     hist, _ = np.histogram(output[:, :, 0], bins=np.arange(180+1))
#     hists.append(hist)
#     #S
#     hist, _ = np.histogram(output[:, :, 1], bins=np.arange(256+1))
#     hists.append(hist)
#     #V
#     hist, _ = np.histogram(output[:, :, 2], bins=np.arange(256+1))
#     hists.append(hist)

#     C = []
#     for h in hists:
#         C.append(k_histogram(h))
#     print("centroids: {0}".format(C))

#     output = output.reshape((-1, c))
#     for i in range(c):
#         channel = output[:, i]
#         index = np.argmin(np.abs(channel[:, np.newaxis] - C[i]), axis=1)
#         output[:, i] = C[i][index]
#     output = output.reshape((x, y, c))
#     output = cv2.cvtColor(output, cv2.COLOR_HSV2RGB)

#     contours, _ = cv2.findContours(edge,
#                                    cv2.RETR_EXTERNAL,
#                                    cv2.CHAIN_APPROX_NONE)
#     # for i in range(len(contours)):
#     #     tmp = contours[i]
#     #     contours[i] = cv2.approxPolyDP(tmp, 2, False)
#     cv2.drawContours(output, contours, -1, 0, thickness=1)
#     return output


# def update_C(C, hist):
#     """
#     update centroids until they don't change
#     """
#     while True:
#         groups = defaultdict(list)
#         #assign pixel values
#         for i in range(len(hist)):
#             if hist[i] == 0:
#                 continue
#             d = np.abs(C-i)
#             index = np.argmin(d)
#             groups[index].append(i)

#         new_C = np.array(C)
#         for i, indice in groups.items():
#             if np.sum(hist[indice]) == 0:
#                 continue
#             new_C[i] = int(np.sum(indice*hist[indice])/np.sum(hist[indice]))
#         if np.sum(new_C-C) == 0:
#             break
#         C = new_C
#     return C, groups


# def k_histogram(hist):
#     """
#     choose the best K for k-means and get the centroids
#     """
#     alpha = 0.001              # p-value threshold for normaltest
#     N = 80                      # minimun group size for normaltest
#     C = np.array([128])

#     while True:
#         C, groups = update_C(C, hist)

#         #start increase K if possible
#         new_C = set()     # use set to avoid same value when seperating centroid
#         for i, indice in groups.items():
#             #if there are not enough values in the group, do not seperate
#             if len(indice) < N:
#                 new_C.add(C[i])
#                 continue

#             # judge whether we should seperate the centroid
#             # by testing if the values of the group is under a
#             # normal distribution
#             z, pval = stats.normaltest(hist[indice])
#             if pval < alpha:
#                 #not a normal dist, seperate
#                 left = 0 if i == 0 else C[i-1]
#                 right = len(hist)-1 if i == len(C)-1 else C[i+1]
#                 delta = right-left
#                 if delta >= 3:
#                     c1 = (C[i]+left)/2
#                     c2 = (C[i]+right)/2
#                     new_C.add(c1)
#                     new_C.add(c2)
#                 else:
#                     # though it is not a normal dist, we have no
#                     # extra space to seperate
#                     new_C.add(C[i])
#             else:
#                 # normal dist, no need to seperate
#                 new_C.add(C[i])
#         if len(new_C) == len(C):
#             break
#         else:
#             C = np.array(sorted(new_C))
#     return C

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     # parser.add_argument('input', help='input image')
#     # parser.add_argument('output', help='output cartoonized image')
#     parser.add_argument('--input', help='input image', default='G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\DataLibrary\\Images\\Hero Heroin\\alia.jpg')
#     parser.add_argument('--output', help='output cartoonized image', default='G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\DataLibrary\\Images\\Hero Heroin\\image------.jpg')


#     args = parser.parse_args()

#     # image = Image.open(args.input)
#     image = cv2.imread(args.input)
#     start_time = time.time()
#     output = cartoonize(image)
#     end_time = time.time()
#     t = end_time-start_time
#     print('time: {0}s'.format(t))
#     cv2.imwrite(args.output, output)


# ======================================================= 
# # videp to cartoon
# import argparse
# import time
# import numpy as np
# import cv2
# from collections import defaultdict
# from scipy import stats

# def cartoonize(image):
#     """
#     Convert image into cartoon-like image
#     image: input image as numpy array
#     """
#     output = np.array(image)
#     x, y, c = output.shape
#     for i in range(c):
#         output[:, :, i] = cv2.bilateralFilter(output[:, :, i], 5, 50, 50)
#     edge = cv2.Canny(output, 100, 200)

#     output = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
#     hists = []
#     for i in range(c):
#         hist, _ = np.histogram(output[:, :, i], bins=np.arange(256+1) if i else np.arange(180+1))
#         hists.append(hist)

#     C = []
#     for h in hists:
#         C.append(k_histogram(h))

#     output = output.reshape((-1, c))
#     for i in range(c):
#         channel = output[:, i]
#         index = np.argmin(np.abs(channel[:, np.newaxis] - C[i]), axis=1)
#         output[:, i] = C[i][index]
#     output = output.reshape((x, y, c))
#     output = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)

#     contours, _ = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#     cv2.drawContours(output, contours, -1, (0, 0, 0), thickness=1)
#     return output

# def update_C(C, hist):
#     """
#     Update centroids until they don't change
#     """
#     while True:
#         groups = defaultdict(list)
#         for i, count in enumerate(hist):
#             if count == 0:
#                 continue
#             d = np.abs(C - i)
#             index = np.argmin(d)
#             groups[index].append(i)

#         new_C = np.array(C)
#         for i, indices in groups.items():
#             new_C[i] = int(np.sum(indices * hist[indices]) / np.sum(hist[indices]))
#         if np.all(new_C == C):
#             break
#         C = new_C
#     return C, groups

# def k_histogram(hist):
#     """
#     Choose the best K for k-means and get the centroids
#     """
#     alpha = 0.001
#     N = 80
#     C = np.array([128])

#     while True:
#         C, groups = update_C(C, hist)
#         new_C = set()
#         for i, indices in groups.items():
#             if len(indices) < N:
#                 new_C.add(C[i])
#                 continue

#             z, pval = stats.normaltest(hist[indices])
#             if pval < alpha:
#                 left = 0 if i == 0 else C[i - 1]
#                 right = len(hist) - 1 if i == len(C) - 1 else C[i + 1]
#                 delta = right - left
#                 if delta >= 3:
#                     new_C.update([(C[i] + left) / 2, (C[i] + right) / 2])
#                 else:
#                     new_C.add(C[i])
#             else:
#                 new_C.add(C[i])
#         if len(new_C) == len(C):
#             break
#         C = np.array(sorted(new_C))
#     return C

# def cartoonize_video(input_video_path, output_video_path):
#     """
#     Convert video into a cartoon-like video.
#     """
#     cap = cv2.VideoCapture(input_video_path)
#     if not cap.isOpened():
#         print("Error: Could not open video.")
#         return

#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = cap.get(cv2.CAP_PROP_FPS)

#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

#     start_time = time.time()

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         cartoon_frame = cartoonize(frame)
#         out.write(cartoon_frame)

#     cap.release()
#     out.release()

#     end_time = time.time()
#     print(f'Video processing time: {end_time - start_time}s')

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--input', help='input video file', default='C:\\Users\\dell\\Downloads\\lovevideo.mp4')
#     parser.add_argument('--output', help='output cartoonized video file', default='C:\\Users\\dell\\Downloads\\output_video.mp4')  
#     args = parser.parse_args()
#     cartoonize_video(args.input, args.output)

# ==================================

# videp to cartoon
import argparse
import time
import dlib
import numpy as np
import cv2
from collections import defaultdict
from scipy import stats

# Load the detector and predictor from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("G:\\Automation_Video_Project\\youtube-autoupload-bot-master\\DataLibrary\\Model\\shape_predictor_68_face_landmarks.dat")  # Ensure you have this model file

def enlarge_eyes(image, factor=1.5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    new_image = image.copy()

    for face in faces:
        landmarks = predictor(gray, face)
        for eye in [list(range(36, 42)), list(range(42, 48))]:  # Indices of eye landmarks
            points = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in eye])
            center = points.mean(axis=0).astype("int")
            radius = int(factor * np.linalg.norm(points[0] - points[3]) / 2)
            eye_mask = np.zeros_like(gray)
            cv2.circle(eye_mask, tuple(center), radius, 255, -1)
            eye_mask = eye_mask.astype(bool)
            
            new_eye = cv2.getRectSubPix(image, (2*radius, 2*radius), tuple(center))
            new_eye = cv2.resize(new_eye, (0, 0), fx=factor, fy=factor)
            new_image[eye_mask] = cv2.getRectSubPix(new_eye, (2*radius, 2*radius), (new_eye.shape[1]/2, new_eye.shape[0]/2))[eye_mask]

    return new_image


def cartoonize(image):
    """
    Convert image into cartoon-like image
    image: input image as numpy array
    """
    output = np.array(image)
    x, y, c = output.shape
    for i in range(c):
        output[:, :, i] = cv2.bilateralFilter(output[:, :, i], 5, 50, 50)
    edge = cv2.Canny(output, 100, 200)

    output = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
    hists = []
    for i in range(c):
        hist, _ = np.histogram(output[:, :, i], bins=np.arange(256+1) if i else np.arange(180+1))
        hists.append(hist)

    C = []
    for h in hists:
        C.append(k_histogram(h))

    output = output.reshape((-1, c))
    for i in range(c):
        channel = output[:, i]
        index = np.argmin(np.abs(channel[:, np.newaxis] - C[i]), axis=1)
        output[:, i] = C[i][index]
    output = output.reshape((x, y, c))
    output = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)

    contours, _ = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(output, contours, -1, (0, 0, 0), thickness=1)
    return output

def update_C(C, hist):
    """
    Update centroids until they don't change
    """
    while True:
        groups = defaultdict(list)
        for i, count in enumerate(hist):
            if count == 0:
                continue
            d = np.abs(C - i)
            index = np.argmin(d)
            groups[index].append(i)

        new_C = np.array(C)
        for i, indices in groups.items():
            new_C[i] = int(np.sum(indices * hist[indices]) / np.sum(hist[indices]))
        if np.all(new_C == C):
            break
        C = new_C
    return C, groups

def k_histogram(hist):
    """
    Choose the best K for k-means and get the centroids
    """
    alpha = 0.001
    N = 80
    C = np.array([128])

    while True:
        C, groups = update_C(C, hist)
        new_C = set()
        for i, indices in groups.items():
            if len(indices) < N:
                new_C.add(C[i])
                continue

            z, pval = stats.normaltest(hist[indices])
            if pval < alpha:
                left = 0 if i == 0 else C[i - 1]
                right = len(hist) - 1 if i == len(C) - 1 else C[i + 1]
                delta = right - left
                if delta >= 3:
                    new_C.update([(C[i] + left) / 2, (C[i] + right) / 2])
                else:
                    new_C.add(C[i])
            else:
                new_C.add(C[i])
        if len(new_C) == len(C):
            break
        C = np.array(sorted(new_C))
    return C

def cartoonize_video(input_video_path, output_video_path):
    """
    Convert video into a cartoon-like video.
    """
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # First apply the cartoonize transformation
        cartoon_frame = cartoonize(frame)
        # Then, apply the enlarge_eyes transformation
        cartoon_frame_with_enlarged_eyes = enlarge_eyes(cartoon_frame, factor=1.5)  # Feel free to change the factor as needed
        # Write the transformed frame to the output video
        out.write(cartoon_frame_with_enlarged_eyes)

    cap.release()
    out.release()

    end_time = time.time()
    print(f'Video processing time: {end_time - start_time}s')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='input video file', default='C:\\Users\\dell\\Downloads\\lovevideo.mp4')
    parser.add_argument('--output', help='output cartoonized video file', default='C:\\Users\\dell\\Downloads\\output_video.mp4')  
    args = parser.parse_args()
    cartoonize_video(args.input, args.output)