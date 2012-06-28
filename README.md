Serveservation
==============

A webapp to manage server reservations

To have an instance up and running, use both commands:
```
./manage.py runserver
sudo ./manage.py celeryd -v 2 -B -s celery -E -l INFO 
```