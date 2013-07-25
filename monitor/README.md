babymonitor
===========

the monitor part  

needed software:   
*   netcat  
*   [mjpeg-streamer](https://code.google.com/p/mjpg-streamer/)  


usage:

edit the Port and Device in start-audio.sh    
and the video device in start-video.sh


*   start-audio.sh make the output of arecord available on $Port via netcat
*   start-video.sh starts the great mjpg-streamer on Port 8080


you can use my precompiled mjpg-streamer version @[the-hawkes.de](http://www.the-hawkes.de/downloads)  
or compile it on your own


Testing:


Live Video should be available @ http://&lt;monitor ip&gt;:8080/?action=stream

Audio:
    start "start-stream-input.sh" on the receiver and 

        aplay <your fifo configured in start-stream-input.sh>
