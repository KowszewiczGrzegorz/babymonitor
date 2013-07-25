#!/usr/bin/python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, jsonify, abort
import alsaaudio
import subprocess
import signal, os
import logging
from logging.handlers import RotatingFileHandler


#Fifo Audio
FILE = "pifone.mp3"
#mjpg stream url
VIDEO = "http://pifone.home:8080"
#log
LOGFILE = "babymonitor.log"

Commands = [ "play",
             "stop",
             "setvolume",
             "status",
           ]


app = Flask(__name__) 
app.config['PROPAGATE_EXCEPTIONS'] = True


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler(LOGFILE, maxBytes=10000, backupCount=5) 
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.debug = True



###########################
class MYAUDIO(object): 
    def __init__(self):
        self.pid = None
        self.connectMixer()
        

    def connectMixer(self):
        #Set Mixer to AlsaMixer
        try:
            self.mixer = alsaaudio.Mixer(control='PCM')
            self.setvolume(95)
        except Exception, e:
            app.logger.error("Error while set Mixer: {0}".format(e))
            abort(503)

    def play(self):
        self.mixer.setmute(0)
        if self.pid is None:
            self.proc = subprocess.Popen(["aplay", FILE], stdout=subprocess.PIPE, 
                                           shell=False, preexec_fn=os.setsid)
            self.pid = self.proc.pid
            app.logger.info("play started pid: {0}".format(self.pid))
        else:
            app.logger.warn("playback already running. PID: {0}".format(self.pid))
        return(self.status())

    def stop(self):
        self.mixer.setmute(1)
        if self.pid is not None:
            os.kill(self.pid, signal.SIGTERM)
            app.logger.info("{0} stopped".format(self.pid))
        self.pid = None
        return(self.status())
        
    
    def status(self):
        vol = self.mixer.getvolume()[0]
        if self.pid is not None:
            sta = "play"
            f   = FILE.split("/")[-1]
        else:
            sta = "stop"
            f   = None
        return({"status" : sta,
                "volume" : vol,
                "current": f})
        
    def setvolume(self, newvol):
        oldvol = self.mixer.getvolume()[0]
        self.mixer.setvolume(int(newvol))
        app.logger.info("Volume changed from {0} to {1}".format(oldvol, newvol))
        return(self.status())


@app.before_first_request
def before_request():
    app.logger.info("Startup")
    global AudioServer
    AudioServer = MYAUDIO()

@app.route("/audio")
def tojson():
    req = request.args.get('cmd', None)
    #args for volume set atm only
    args = request.args.get('args', None)
    if req not in Commands:
        return('unknown command {0}'.format(req))
    if args:
        if not 0 <= int(args) <= 100:
            return('args out of range {0}'.format(args))
        return(jsonify(getattr(AudioServer, req)(args)))
    return(jsonify(getattr(AudioServer, req)()))

@app.route("/")
def index():
    return(render_template("index.html", videoUrl=VIDEO ))

if __name__ == "__main__":
    app.debug = True
    #app.run('0.0.0.0')
    app.run()
