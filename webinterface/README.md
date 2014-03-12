babymonitor
the webinterface

![Screenshot](https://github.com/thehawkes/babymonitor/raw/master/screenshot.jpg)

build with:
*   [flask](http://flask.pocoo.org/)
*   [twitter bootstrap](http://twitter.github.io/bootstrap/)
*   [jquery](http://jquery.com/)


dependencies:
*   python-alsaaudio
*   python-flask


usage:
*   edit babymonitor.py
    change the following options if needed:

        HOST = '0.0.0.0'
        PORT = 8080
        AUDIO = 'stream'
        AUDIOSTREAM = 'http://babymon.home:8000/baby'
        ALT_AUDIOSTREAM = None
        FILE = 'pifone.mp3'
        PLAY = 'aplay'
        VIDEO = True
        VIDEOURL = 'http://192.168.178.52/mjpeg.cgi'
        LOGFILE = '/var/www/logs/babymonitor.log'

only 1 AUDIO type is supported (fifo or stream)


as standalone:

        python babymonitor.py

the website will be available (default settings)@

        http://<<your server ip>>:8080


with nginx & gunicorn:

    apt-get update; apt-get install gunicorn nginx


create a new gunicron config

    vi /etc/gunicron.d/babymonitor.ini
add

    CONFIG = {
    'working_dir': '<<path to the babymonitor directory>>',
    'args': (
        '--bind=127.0.0.1:8000',
        '--workers=1',
        '--timeout=60',
        '--user=root',
        '--group=www-data',
        #'--log-level=debug',
        'babymonitor:app',
    ),
    }
restart

    /etc/init.d/gunicorn restart


add a site to nginx

    vi /etc/nginx/sites-available/babymonitor
add

    server {
        listen 80;
        server_name _;
        root <<path to the babymonitor directory>>;

        location / {
            try_files $uri @proxy;
        }

        location @proxy {
            proxy_pass http://127.0.0.1:8000;
        }
    }

restart

    /etc/init.d/nginx restart


the website should be up on http://&lt;your receiver ip&gt;
