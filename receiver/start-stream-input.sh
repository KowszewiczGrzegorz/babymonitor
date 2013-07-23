#!/bin/bash
# 
#  create the fifo and pipe the netcat output to it
#
#


pipe="/var/www/babyfone/pifone.mp3"

if [[ ! -p $pipe ]]; then
    mkfifo $pipe
fi
    
while true
do 
    echo "Press and hold [CTRL+C] to stop.."

    netcat -v pifone.home 5000 > $pipe
done

