import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

# Need gstreamer

import cv2 
import time
from utils import get_current_average_fps, get_image_file_name
from server import Realtime_Server



cv2.namedWindow("preview")


camera = cv2.VideoCapture(0, cv2.CAP_MSMF)
#camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m', 'j', 'p', 'g'))
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

# Make image directories
image_dir = os.path.join(os.getcwd(), "images")
if not os.path.isdir(image_dir):
    os.makedirs(image_dir)


# Initialize server
rtserver = Realtime_Server()
rtserver.start_server_in_new_thread()



last_frame_time_ns = time.time_ns()

last_capture_time_ns = time.time_ns()
capture_interval = 1000000000/30 
capture_image_index = 0


while camera.isOpened(): # try to get the first frame
    rval, frame = camera.read()
    cur_time_ns = time.time_ns()


    cv2.imshow("preview", frame)


    fps = get_current_average_fps(cur_time_ns - last_frame_time_ns)
    print(f"fps: {fps}")
    last_frame_time_ns = cur_time_ns

    if (cur_time_ns - last_capture_time_ns) > capture_interval:
        last_capture_time_ns += capture_interval
        file_name = get_image_file_name(capture_image_index)
        capture_image_index += 1

        #cv2.imwrite(os.path.join(image_dir, file_name), frame)


    rtserver.stream_frame({"frame": frame})


    key = cv2.waitKey(1)
    if key == ord("q"):
        break 



camera.release()
cv2.destroyWindow("preview")