#!/bin/sh
dockerize -wait tcp://db:5432 -timeout 20s
python3 manage.py db upgrade
python3 manage.py runserver -h 0.0.0.0 $*
