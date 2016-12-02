# RosReestr XML Parcels Parser

## Django-based Web Application

Development (or local usage) setup:

```bash
cd backend
virtualenv -p `which python3` venv
. venv/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver_plus
# go to localhost:8000, where you can upload files
# there is also an administrative interface
# for the database at localhost:8000/admin
# use ./manage.py createsuperuser to get access there
```

## Production Deploy Setup

0. Choose/create a user to run the project as. We'll assume you're using `rrp`/`webapps`.
1. First, follow development setup instructions.
2. Then, install `gunicorn` (`pip install gunicorn`), create a run script (see example below), and test it.
3. Setup supervision for the run script (see `supervisord` example below), and test it.
4. Setup http-server host configuration (see `nginx` config example below), and test it.
5. Enjoy.

### Gunicorn Run Script Example  

TODO

### Supervisord Config Example

TODO

### Nginx Site Config Example

TODO