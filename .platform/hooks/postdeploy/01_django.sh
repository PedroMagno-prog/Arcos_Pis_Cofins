#!/bin/bash
set -e
source /var/app/venv/*/bin/activate
python manage.py migrate --noinput
python manage.py findstatic bootstrap/css/bootstrap.min.css
python manage.py findstatic js/jquery-3.7.1.min.js
python manage.py collectstatic --noinput
