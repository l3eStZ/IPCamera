import os
import signal
import onvifconfig
import subprocess
import time
import sys
from CameraControl import CameraControl

# output_path = f'home/test/workspace/camera/VideoFile'
# framerate = 20
output_path = f'home/test/workspace/lab/rstp_relay/src'
stream_link = f'rtsp://root:12345@192.168.10.232/stream=0'

if __name__ == "__main__":
    status = os.system(f'ffmpeg -rtsp_transport tcp \
            -i {stream_link} \
            -stimeout 3000 \
            -strftime 1 \
            -b:v 1200 \
            -f segment \
            -segment_list "{output_path}/videoList.m3u8" \
            -segment_list_size 5 \
            -segment_time 20 \
            -min_seg_duration 18 \
            -reset_timestamps 1 \
            "{output_path}/VideoFile/video_output_%Y%m%d-%H%M%S.ts" ')