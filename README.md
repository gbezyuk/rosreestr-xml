# RosReestr XML Parcels Parser

Just a helping tool project for a friend of mine. There are a standalone script and a django-based web application in this repo. 

## Standalone Parser Script

See `/standalone_script/parse.py`. Uses RosReestr XML files as an input, produces JSON dictionaries and CSV files as outputs.

Usage:

```bash
> ./parse.py ./data-samples/doc14350111.xml -j ./test.json -c ./test.csv -v
Parsing original document...
Parsing original document DONE
Storing JSON file...
Storing JSON file DONE
Extracting Parcels...
Extracting Parcels DONE
Storing CSV file...
Storing CSV file DONE
```

See `./parse.py -h` for more information on parameters.

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

See `/backend/README.md` for details.