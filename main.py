import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"


# Need gstreamer

import cv2 
import time
from utils import get_current_average_fps, get_image_file_name, get_latest_image_index
from server import Realtime_Server


# 1. Health endpoint
# 2. Try catch to restart connecting to the CAMERA once crashed
# 3. Extract video index, then pick up index if crashed

cv2.namedWindow("preview")


CAMERA = None
def initialize_camera():
    cam = cv2.VideoCapture(0, cv2.CAP_MSMF)
    #cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m', 'j', 'p', 'g'))
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    return cam



# Make image directories
image_dir = os.path.join(os.getcwd(), "images")
if not os.path.isdir(image_dir):
    os.makedirs(image_dir)


# Initialize server
rtserver = Realtime_Server()
rtserver.start_server_in_new_thread()



last_frame_time_ns = time.time_ns()

last_capture_time_ns = time.time_ns()
capture_interval = 1000000000/5
capture_image_index = 0

user_quit = False

while user_quit == False:

    if CAMERA == None or not CAMERA.isOpened():
        try:
            CAMERA = initialize_camera()
            capture_image_index = get_latest_image_index(image_dir)
            
        except Exception as e:
            print("Exception --------------------------------------------------------")
            print(e)
            CAMERA = None


    try:
        if (not CAMERA is None) and CAMERA.isOpened(): # try to get the first frame
            rval, frame = CAMERA.read()
            cur_time_ns = time.time_ns()

            if frame is None:
                raise Exception("Frame is none bucko")

            cv2.imshow("preview", frame)


            fps = get_current_average_fps(cur_time_ns - last_frame_time_ns)
            print(f"fps: {fps}")
            last_frame_time_ns = cur_time_ns

            if (cur_time_ns - last_capture_time_ns) > capture_interval:
                last_capture_time_ns += capture_interval
                file_name = get_image_file_name(capture_image_index)
                capture_image_index += 1

                cv2.imwrite(os.path.join(image_dir, file_name), frame)


            rtserver.stream_frame({"frame": frame})

    except Exception as e: 
        print("Exception --------------------------------------------------------")
        print(e)
        CAMERA = None
        # Sleep for one second before trying again
        time.sleep(1)


    key = cv2.waitKey(1)
    if key == ord("q"):
        user_quit = True



CAMERA.release()
cv2.destroyWindow("preview")