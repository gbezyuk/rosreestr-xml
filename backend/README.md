# RosReestr XML Parcels Parser

## Django-based Web Application

Development (or local usage) setup:

```bash
cd backend
virtualenv -p `which python3` venv # create virtual environment to isolate dependencies
. venv/activate # activate it
pip install -r requirements.txt # install dependencies
cd parcel && ../manage.py compilemessages -l ru && cd .. # compile translation files
./manage.py migrate # init database
./manage.py runserver_plus # run dev server
# go to localhost:8000, where you can upload files
# there is also an administrative interface
# for the database at localhost:8000/admin
# use ./manage.py createsuperuser to get access there
```

## Production Deploy Setup

0. Choose/create a user to run the project as. We'll assume you're using `rrp`/`webapps`.
1. Follow development setup instructions.
2. Collect static files with `./manage.py collectstatic`
3. Install `gunicorn` (`pip install gunicorn`), create a run script (see example below), and test it.
4. Setup supervision for the run script (see `supervisord` example below), and test it.
5. Setup http-server host configuration (see `nginx` config example below), and test it.
6. Enjoy.

### Gunicorn Run Script Example  

```bash
#!/bin/bash
# supposed to be located at /webapps/rrp/backend/bin/gunicorn_start.sh
NAME="rrp"
DJANGODIR=/webapps/rrp/backend
SOCKFILE=/webapps/rrp/backend/run/gunicorn.sock     # dir should exist with proper access rights
USER=rrp
GROUP=webapps
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=rrp.settings
DJANGO_WSGI_MODULE=rrp.wsgi

echo "Starting $NAME as `whoami`"

cd $DJANGODIR
. /webapps/rrp/backend/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE
```

### Supervisord Config Example

```ini
[program:rrp_backend]
command = /webapps/rrp/backend/bin/gunicorn_start
user = rrp
stdout_logfile = /webapps/rrp/backend/logs/gunicorn_supervisor.log
redirect_stderr = true
autostart=true
autorestart=unexpected
```

### Nginx Site Config Example

```ini
# make sure to use the name specified in ALLOWED_HOSTS
upstream backend.parcel.gbezyuk.ru {
  server unix:/webapps/rrp/backend/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name parcel.gbezyuk.ru;

    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;

    client_max_body_size 4G;

    access_log /webapps/rrp/backend/logs/nginx-access.log;
    error_log /webapps/rrp/backend/logs/nginx-error.log;

    location /static/ {
        alias   /webapps/rrp/backend/static/;
    }
    location /media/ {
        alias   /webapps/rrp/backend/media/;
    }

    location / {
        if (!-f $request_filename) {
            proxy_pass http://backend.parcel.gbezyuk.ru;
            break;
        }
    }
}
```