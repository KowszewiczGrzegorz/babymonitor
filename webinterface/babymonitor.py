#!/usr/bin/python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, jsonify, abort
import alsaaudio
import subprocess
import signal
import os
import logging
from logging.handlers import RotatingFileHandler


'''
    Webinterface Settings
'''
#default listen on all interfaces
HOST = '0.0.0.0'
#default port 8080
PORT = 8080

'''
    AUDIO Settings
    choose between:
        stream (like darkice+icecast)
        fifo (like http://www.the-hawkes.de/a-raspberry-pi-powered-baby-monitor-12.html)
'''
AUDIO = 'stream'

#stream settings
AUDIOSTREAM = 'http://babymon.home:8000/baby'
ALT_AUDIOSTREAM = None

#fifo settings
FILE = 'pifone.mp3'
#fifo playback command
PLAY = 'aplay'

'''
    Video Settings
'''
VIDEO = True
#mjpg stream url
#VIDEO = 'http://pifone.home:8080'
# DCS-932L video url
VIDEOURL = 'http://192.168.178.52/mjpeg.cgi'

'''
    Log Settings
'''
LOGFILE = '/var/www/logs/babymonitor.log'


DEBUG = True


######################################################
### only edit below if you know what you are doing ###
######################################################

Commands = [ 'play',
             'stop',
             'setvolume',
             'status',
           ]

AudioServer = None

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.debug = DEBUG


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler(LOGFILE, maxBytes=10000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.addHandler(handler)


'''
    FIFO Audio Class

    Includes:
        - Alsa Mixer Control to control the volume on the receiver
        - Aplay to playback the local fifo file

'''


class FIFOAUDIO(object):
    def __init__(self):
        self.pid = None
        self.connectMixer()

    def connectMixer(self):
        try:
            self.mixer = alsaaudio.Mixer(control='PCM')
            self.setvolume(95)
        except Exception, e:
            app.logger.error('Error while set Mixer: {0}'.format(e))
            abort(500)

    def play(self):
        self.mixer.setmute(0)
        if self.pid is None:
            self.proc = subprocess.Popen([PLAY, FILE], stdout=subprocess.PIPE,
                                         shell=False, preexec_fn=os.setsid)
            self.pid = self.proc.pid
            app.logger.info('play started pid: {0}'.format(self.pid))
        else:
            app.logger.warn('playback already running. PID: {0}'.format(self.pid))
        return(self.status())

    def stop(self):
        self.mixer.setmute(1)
        if self.pid is not None:
            os.kill(self.pid, signal.SIGTERM)
            app.logger.info('{0} stopped'.format(self.pid))
        self.pid = None
        return(self.status())

    def status(self):
        vol = self.mixer.getvolume()[0]
        if self.pid is not None:
            sta = 'play'
            f   = FILE.split('/')[-1]
        else:
            sta = 'stop'
            f   =  None
        return({'status' : sta,
                'volume' : vol,
                'current': f})

    def setvolume(self, newvol):
        oldvol = self.mixer.getvolume()[0]
        self.mixer.setvolume(int(newvol))
        app.logger.info('Volume changed from {0} to {1}'.format(oldvol, newvol))
        return(self.status())

'''
    Flask Part
'''

'''
    Error Handling
'''


@app.errorhandler(500)
def internal_error(error):
    return render_template('5xx.html', log=LOGFILE), 500


@app.before_first_request
def before_request():
    global AudioServer
    if AUDIO == 'fifo':
        AudioServer = FIFOAUDIO()
    elif AUDIO == 'stream':
        #nothing todo yet
        pass
    else:
        app.logger.error('Unkown Audiotyp: {0}'.format(AUDIO))
        abort(500)
    app.logger.info('Startup with Audio: {0}'.format(AUDIO))

'''
    Routing Part
'''


@app.route('/audio')
def audio():
    if AUDIO == 'fifo':
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
    else:
        return(jsonify({'Error': 'AudioServer disabled if {0} is set'.format(AUDIO)}))


@app.route('/')
def index():
    return(render_template('index.html',
                            videoUrl=VIDEOURL,
                            audiotyp=AUDIO,
                            audiostream=AUDIOSTREAM,
                            alt_audiostream=ALT_AUDIOSTREAM))


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
