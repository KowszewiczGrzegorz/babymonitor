#!/bin/bash
mjpg_streamer -i "libinput_uvc.so.0 -d /dev/video0 -f 24" -o "liboutput_http.so.0 -p 8080"
