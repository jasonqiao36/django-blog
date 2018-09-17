#!/bin/sh
python /webapp/manage.py collectstatic --noinput
/usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/webapp
