import datetime
import os

average_frame_time_ns_array = []
average_frame_time_ns_max_count = 30
total_average_frame_time_ns = 0

def get_current_average_fps(new_frame_time_ns: float):
    global average_frame_time_ns_array, average_frame_time_ns_max_count, total_average_frame_time_ns

    if len(average_frame_time_ns_array) > average_frame_time_ns_max_count:
        removed_frame_time_ns = average_frame_time_ns_array.pop(0)
        total_average_frame_time_ns -= removed_frame_time_ns

    average_frame_time_ns_array.append(new_frame_time_ns)
    total_average_frame_time_ns += new_frame_time_ns

    average_frame_time_ns = total_average_frame_time_ns / len(average_frame_time_ns_array) 
    fps = int(1000000000.0 / average_frame_time_ns)
    return fps
    

index_string_width = 10
def get_image_file_name(image_index: int):
    
    date_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file_name = f"{str(image_index).rjust(index_string_width, "0")}_{date_time}.png"

    return file_name


# Make image directories
def get_latest_image_index(image_dir: str):
    images = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

    if len(images) == 0:
        return 0
    latest_image = images[-1]
    temp_array = latest_image.split("_")
    temp_str = temp_array[0]
    while len(temp_str) > 0 and temp_str[0] == "0":
        temp_str = temp_str[1:]

    latest_index = int(temp_array[0]) + 1
    return latest_index
