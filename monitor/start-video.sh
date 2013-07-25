#!/bin/bash
RESOLUTION="640x480"
FPS="24"
PORT="8080"
mjpg_streamer -i "libinput_uvc.so.0 -d /dev/video0 -r $RESOLUTION -f $FPS" -o "liboutput_http.so.0 -p $PORT"
