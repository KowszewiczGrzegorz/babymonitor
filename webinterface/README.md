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
*   change FILE, VIDEO & LOGFILE according to your setup  

as standalone:

        python babymonitor.py

the website will be available @

        http://127.0.0.1:5000


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
