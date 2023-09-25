import os
import onvifconfig
from CameraControl import CameraControl

output_path = f'./VideoFile'
stream_link = f'rtsp://admin:Test1234@192.168.1.105/stream=0'

if __name__ == "__main__":
    # ptz = onvifconfig.ptzcam("192.168.1.105", 80, "admin", "Test1234", "./wsdl")
    # camera_control = CameraControl(ptz)
    # key = None

    status = os.system(f'ffmpeg -rtsp_transport tcp \
            -i {stream_link} \
            -stimeout 3000 \
            -strftime 1 \
            -b:v 1200 \
            -f segment \
            -segment_list "{output_path}/videoList.m3u8" \
            -segment_list_size 5 \
            -segment_time 20 \
            -reset_timestamps 1 \
            "{output_path}/video_output_%Y%m%d-%H%M%S.ts" ')

    # while key != "q":
    #     key = input("Insert key : ")
    #     camera_control.control(key)
    