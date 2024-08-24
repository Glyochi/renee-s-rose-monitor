import datetime

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