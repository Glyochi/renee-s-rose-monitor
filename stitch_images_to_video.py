import os

import cv2



# Make image directories
image_dir = f"{os.getcwd()}/images"


image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]


temp_image = cv2.imread(image_paths[0])
video_height, video_width, _ = temp_image.shape

video_path = os.path.join(os.getcwd(), "video.mp4")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_path, -1, 30, (video_width, video_height))

for path in image_paths:

    image = cv2.imread(path)
    video.write(image)
    print(path)
