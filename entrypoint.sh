#!/bin/sh
python manage.py collectstatic
python manage.py makemigrations miditheatre
python manage.py makemigrations
python manage.py migrate
python manage.py runserver